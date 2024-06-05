import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Set

import osparc
import osparc._models
import pydantic
import pytest

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
    output = subprocess.run(
        cmd, cwd=source_package, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert output.returncode == 0
    import_dependencies: Set[str] = set(import_file.read_text().splitlines())

    # generate requirements file based on installed osparc
    cmd: list[str] = [
        "pipdeptree",
        "-p",
        "osparc",
        "--json",
    ]
    output = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert output.returncode == 0
    dep_tree: List[Dict[str, Any]] = json.loads(output.stdout)
    dep_tree = [elm for elm in dep_tree if elm["package"]["key"] == "osparc"]
    assert len(dep_tree) == 1
    install_dependencies: Set(str) = {
        dep["package_name"].replace("-", "_") for dep in dep_tree[0]["dependencies"]
    }
    msg: str = (
        "imported dependencies not specified "
        f"in setup.py: {import_dependencies - install_dependencies}\n"
        "setup.py dependencies which are "
        f"not imported: {install_dependencies - import_dependencies}"
    )
    assert import_dependencies == install_dependencies, msg


@pytest.mark.parametrize("valid", [True, False])
def test_parent_project_validation(faker, valid: bool):
    if valid:
        os.environ["OSPARC_STUDY_ID"] = f"{faker.uuid4()}"
        os.environ["OSPARC_NODE_ID"] = f"{faker.uuid4()}"
        parent_info = osparc._models.ParentProjectInfo()
        assert parent_info.x_simcore_parent_project_uuid is not None
        assert parent_info.x_simcore_parent_node_id is not None
    else:
        os.environ["OSPARC_STUDY_ID"] = f"{faker.text()}"
        os.environ["OSPARC_NODE_ID"] = f"{faker.text()}"
        with pytest.raises(pydantic.ValidationError):
            _ = osparc._models.ParentProjectInfo()
