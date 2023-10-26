import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

import osparc

_PYTHON_DIR: Path = Path(__file__).parent.parent.parent


def test_get_api():
    info = osparc.openapi()
    assert isinstance(info["info"]["version"], str)


def test_dependencies(tmp_path: Path):
    """
    Ensure packages which are imported in osparc are also specified in setup.py
    """
    # get imported packages
    import_file: Path = tmp_path / "imported_packages.txt"
    source_package: Path = _PYTHON_DIR / "client" / "osparc"
    assert source_package.is_dir()
    cmd: list[str] = [
        "pipreqs",
        "--savepath",
        str(import_file.resolve()),
        "--mode",
        "no-pin",
    ]
    output = subprocess.run(cmd, capture_output=True, text=True, cwd=source_package)
    assert output.returncode == 0
    import_dependencies: Set[str] = set(import_file.read_text().splitlines())

    # generate requirements file based on installed osparc
    cmd: list[str] = [
        sys.executable,
        "-m",
        "pipdeptree",
        "-p",
        "osparc",
        "--json",
    ]
    output = subprocess.run(cmd, capture_output=True, text=True)
    assert output.returncode == 0
    dep_tree: List[Dict[str, Any]] = json.loads(output.stdout)
    dep_tree = [elm for elm in dep_tree if elm["package"]["key"] == "osparc"]
    assert len(dep_tree) == 1
    install_dependencies: Set(str) = {
        dep["package_name"].replace("-", "_") for dep in dep_tree[0]["dependencies"]
    }
    assert import_dependencies == install_dependencies
