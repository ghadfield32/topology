#!/usr/bin/env pwsh
# Verify the committed revision in a FRESH checkout: exports HEAD via git archive,
# then confirms the generated workbook inventory matches the generator exactly.
#
# This answers "is the committed work reproducible?", which a dirty working tree
# cannot answer. It does not need the course venv: the generator is stdlib-only
# and only reads native/protocols/labs.json.

param([string]$Revision = 'HEAD')

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ('shape-fresh-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff'))
New-Item -ItemType Directory -Path $tmp | Out-Null

try {
    Write-Host "Exporting $Revision to $tmp ..." -ForegroundColor Cyan
    # Write the archive to a FILE first. Piping a binary tar through PowerShell's
    # text pipeline corrupts it ("bad header checksum").
    $tar = Join-Path ([System.IO.Path]::GetTempPath()) ('shape-' + [guid]::NewGuid().ToString('N') + '.tar')
    git archive --format=tar -o $tar $Revision
    if ($LASTEXITCODE -ne 0) { throw "git archive failed" }
    tar -xf $tar -C $tmp
    if ($LASTEXITCODE -ne 0) { throw "tar extract failed" }
    Remove-Item -LiteralPath $tar -Force -ErrorAction SilentlyContinue

    Write-Host "`nInventory in the fresh checkout:" -ForegroundColor Cyan
    $nb = (Get-ChildItem (Join-Path $tmp 'workbooks/polyglot') -Recurse -Filter '*.ipynb' | Measure-Object).Count
    Write-Host "  notebooks: $nb"
    foreach ($f in @('native/protocols/labs.json', 'curriculum/catalog.json', 'native_course.py',
                     'tools/build_language_notebooks.py', 'tools/verify_language_notebooks.py',
                     'tools/evidence_pointer.py', 'uv.lock')) {
        $ok = Test-Path (Join-Path $tmp $f)
        Write-Host ("  {0,-45} {1}" -f $f, $(if ($ok) { 'present' } else { 'MISSING' }))
    }

    Write-Host "`nGenerator check against the fresh checkout:" -ForegroundColor Cyan
    $py = Join-Path $repo '.venv\Scripts\python.exe'
    if (-not (Test-Path $py)) { $py = 'python' }
    & $py (Join-Path $tmp 'tools/build_language_notebooks.py') --check
    $rc = $LASTEXITCODE
    Write-Host "generator --check exit: $rc"
    if ($rc -ne 0) { throw "fresh checkout does not reproduce the generated inventory" }

    Write-Host "`nFRESH CHECKOUT OK" -ForegroundColor Green
}
finally {
    if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue }
}
