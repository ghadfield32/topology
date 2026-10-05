"""Hash and export actual run outputs, never publish them or grade a learner.

Hashes establish local byte continuity, not authorship, measurement truth, or
scientific significance. Legacy runs without an output seal need a fresh replay.
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
from pathlib import Path
import shutil
from typing import Any

REFLECTION_FIELDS = ('question', 'observation_unit', 'method',
                     'result_interpretation', 'limitation', 'next_experiment')


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(part)
    return h.hexdigest()


def _file(root: Path, relative: str) -> Path:
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts or not relative or '\\' in relative:
        raise ValueError('Unsafe output path: ' + relative)
    result = root / p
    if result.is_symlink() or not result.resolve().is_relative_to(root.resolve()):
        raise ValueError('Output symlink/path escape: ' + relative)
    # Reject a symlink in any parent, even one currently pointing inside the run.
    if any((root / Path(*p.parts[:n])).is_symlink() for n in range(1, len(p.parts))):
        raise ValueError('Output has a symlink parent: ' + relative)
    return result


def _outputs(run: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for directory in ('executed', 'artifacts'):
        base = run / directory
        if base.is_symlink():
            raise ValueError('Output directory is a symlink.')
        if not base.exists():
            continue
        for p in sorted(base.rglob('*')):
            rel = p.relative_to(run).as_posix()
            if p.is_symlink():
                raise ValueError('Output symlink: ' + rel)
            if p.is_file():
                found[rel] = digest(_file(run, rel))
    return found


def seal_run(run: Path, report: dict[str, Any]) -> None:
    """Add an output inventory to a run report, including failed-run evidence.

    Does not mutate file outputs or certify their correctness. The caller writes
    the amended execution.json after computing the hashes.
    """
    report['output_seal_schema'] = 1
    report['output_sha256'] = _outputs(Path(run))
    report['output_seal_scope'] = 'Executed notebooks and generated artifacts; local continuity, not a signature.'


def validate_run(run: Path) -> list[str]:
    """Reject incomplete, failed, changed, or unsafe run outputs before export."""
    import nbformat
    run = Path(run).resolve()
    errors: list[str] = []
    try:
        r = json.loads(_file(run, 'execution.json').read_text(encoding='utf-8'))
        expected = r.get('order', [])
        records = r.get('records', [])
        paths = [x.get('path') for x in records]
        if not expected or len(expected) != len(set(expected)) or set(expected) != set(paths) or len(paths) != len(set(paths)):
            errors.append('Incomplete or duplicate reference identities.')
        if any(type(r.get(k)) is not int for k in ('passed','failed')) or r.get('passed') != len(expected) or r.get('failed') != 0 or not expected:
            errors.append('Run did not complete every expected reference.')
        if r.get('source_inputs_unchanged') is not True:
            errors.append('Source input continuity was not established.')
        if r.get('required_prior_reports_copied') is not False or r.get('mode') != 'fresh_input_workspace_and_fresh_kernels':
            errors.append('Fresh execution mode was not established.')
        seal = r.get('output_sha256', {})
        if type(r.get('output_seal_schema')) is not int or r.get('output_seal_schema') != 1 or not seal:
            errors.append('Missing output seal; replay this reference with the current runner.')
        current = _outputs(run)
        if set(current) != set(seal):
            errors.append('Output file inventory changed or is incomplete.')
        for rel, checksum in seal.items():
            _file(run, rel)
            if current.get(rel) != checksum:
                errors.append('Changed or missing output: ' + rel)
        for rec in records:
            p = rec.get('path', '')
            rel = 'executed/' + p
            if rel not in seal:
                errors.append('Reference notebook not in output seal: ' + p)
                continue
            if rec.get('status') != 'passed' or type(rec.get('source_code_cells')) is not int or rec['source_code_cells'] < 1:
                errors.append('Reference did not execute its teaching cells: ' + p)
                continue
            book = nbformat.read(_file(run, rel), as_version=4)
            cells = [c for c in book.cells if c.cell_type == 'code']
            expected_cells = rec['source_code_cells'] + rec.get('runtime_probe_cells', 0)
            if len(cells) != expected_cells or any(c.execution_count is None for c in cells):
                errors.append('Incomplete executed cells: ' + p)
            if any(o.output_type == 'error' for c in cells for o in c.get('outputs', [])):
                errors.append('Error output in reference: ' + p)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        errors.append(f'Invalid run evidence: {type(exc).__name__}: {exc}')
    return errors


def _shell(title: str, body: str) -> str:
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>''' + html.escape(title) + '''</title><style>
body{font:17px/1.65 system-ui,sans-serif;max-width:1080px;margin:3rem auto;padding:0 1.3rem;color:#17333b;background:#f8faf8}
a{color:#086865}h1{font-size:2.3rem;line-height:1.15}h2{margin-top:2rem}
pre{white-space:pre-wrap;overflow-wrap:anywhere;padding:1rem;background:#e9f0ed;border-radius:8px;font-size:.91rem}
article{background:white;border:1px solid #d6e0db;border-radius:10px;padding:1.2rem;margin:1.2rem 0}
.notice{border-left:4px solid #aa6814;padding:.7rem 1rem;background:#fff3de}
img{max-width:100%;height:auto}li{margin:.45rem 0}code{overflow-wrap:anywhere}
</style></head><body>''' + body + '</body></html>'


def _render_notebook(source: Path, output: Path) -> None:
    """Display code/text/PNG only. Never embed arbitrary HTML, JS, or SVG outputs."""
    import nbformat
    book = nbformat.read(source, as_version=4)
    parts = ['<h1>' + html.escape(source.name) + '</h1>',
             '<p class="notice">Saved executed evidence. HTML/JavaScript/SVG notebook outputs are not executed or embedded here.</p>']
    for index, cell in enumerate(book.cells):
        parts.append('<article><h2>' + ('Explanation' if cell.cell_type == 'markdown' else 'Code') + f' · {index + 1}</h2>')
        parts.append('<pre>' + html.escape(cell.source) + '</pre>')
        for number, out in enumerate(cell.get('outputs', [])):
            if out.get('output_type') == 'stream':
                parts.append('<h3>Observed output</h3><pre>' + html.escape(out.get('text', '')) + '</pre>')
            data = out.get('data', {})
            if 'text/plain' in data:
                parts.append('<pre>' + html.escape(data['text/plain']) + '</pre>')
            if 'image/png' in data:
                raw = base64.b64decode(data['image/png'], validate=False)
                if not raw.startswith(b'\x89PNG\r\n\x1a\n'):
                    raise ValueError('Invalid PNG output.')
                image = f'{output.stem}-{index}-{number}.png'
                (output.parent / image).write_bytes(raw)
                parts.append('<img alt="Saved experiment figure" src="' + html.escape(image, quote=True) + '">')
        parts.append('</article>')
    output.write_text(_shell(source.name, ''.join(parts)), encoding='utf-8')


def export_packet(run: Path, output: Path, reflection: dict[str, Any]) -> dict[str, Any]:
    """Create a local draft report with evidence; never upload or imply mastery.

    The six reflection fields are required learner statements, not automatically
    verified conclusions. The packet may include third-party data/results; review
    licenses and identifying information before choosing to share it.
    """
    if not all(isinstance(reflection.get(k), str) and reflection[k].strip() for k in REFLECTION_FIELDS):
        raise ValueError('Complete all six reflection fields first; this is a completeness check, not grading.')
    run = Path(run).resolve(); output = Path(output).resolve()
    if output.exists():
        raise FileExistsError('Output exists; choose a new report directory.')
    if output.is_relative_to(run):
        raise ValueError('Place the report outside its input run directory.')
    errors = validate_run(run)
    if errors:
        raise ValueError('Run evidence was not accepted: ' + '; '.join(errors))
    output.mkdir(parents=True, exist_ok=False)
    r = json.loads((run / 'execution.json').read_text())
    pages = []
    for rec in r['records']:
        relative = Path('notebooks') / Path(rec['path']).with_suffix('.html')
        target = output / relative; target.parent.mkdir(parents=True, exist_ok=True)
        _render_notebook(_file(run, 'executed/' + rec['path']), target)
        pages.append((relative.as_posix(), rec['path']))
    # Preserve the exact output files and ledger for independent inspection.
    for rel in r['output_sha256']:
        target = output / 'evidence' / rel; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(_file(run, rel), target)
    shutil.copyfile(run / 'execution.json', output / 'evidence/execution.json')
    (output / 'reflection.json').write_text(json.dumps(reflection, indent=2) + '\n', encoding='utf-8')
    body = '<h1>My experiment evidence</h1><p class="notice">Local draft, not publicly published. Review paths, identities and data licenses before sharing. Successful execution is not a scientific guarantee or an assessment of mastery.</p>'
    for key in REFLECTION_FIELDS:
        body += '<h2>' + html.escape(key.replace('_', ' ').capitalize()) + '</h2><p>' + html.escape(reflection[key]) + '</p>'
    body += '<h2>Executed code and observed outputs</h2><ul>' + ''.join('<li><a href="' + html.escape(p, quote=True) + '">' + html.escape(label) + '</a></li>' for p, label in pages) + '</ul>'
    body += '<p><a href="evidence/execution.json">Execution ledger and output hashes</a> · <a href="reflection.json">Learner reflection</a></p>'
    (output / 'index.html').write_text(_shell('Experiment evidence', body), encoding='utf-8')
    # Recheck after copying; a concurrently changed source cannot create a pass.
    if validate_run(run) or any(digest(output/'evidence'/p) != h for p,h in r['output_sha256'].items()):
        raise ValueError('Source outputs changed during export; packet is not accepted.')
    packet_files = {p.relative_to(output).as_posix(): digest(p) for p in sorted(output.rglob('*')) if p.is_file()}
    result = {'status':'passed', 'published':False, 'learner_assessment':'not_assessed',
              'source_ledger_sha256':digest(run/'execution.json'), 'notebooks':len(pages),
              'files_sha256':packet_files, 'reflection_validation':'Completeness only; not truth or correctness.',
              'scope':'Portable local evidence draft; output hashes establish continuity, not authorship or scientific validity.'}
    (output/'packet.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result
