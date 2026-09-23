from pathlib import Path
import tomllib
import shape_lab

def test_distribution_and_module_versions_agree():
    metadata=tomllib.loads((Path(__file__).resolve().parents[1]/'pyproject.toml').read_text())
    assert shape_lab.__version__==metadata['project']['version']=='12.0.0'
