import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Set
from faker import Faker
import osparc
import osparc._settings
import pydantic
import pytest

_CLIENTS_PYTHON_DIR: Path = Path(__file__).parent.parent.parent


def test_get_api():
    info = osparc.openapi()
    assert isinstance(info["info"]["version"], str)


def test_dependencies(tmp_path: Path):
    """
    Ensure packages which are imported in osparc are also specified in setup.py
    """
    # get in-code imported packages
    import_file: Path = tmp_path / "imported_packages.txt"
    source_package: Path = _CLIENTS_PYTHON_DIR / "src" / "osparc"
    assert source_package.is_dir()

    subprocess.run(
        [
            "pipreqs",
            "--savepath",
            str(import_file.resolve()),
            "--mode",
            "no-pin",
        ],
        cwd=source_package,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    import_dependencies: Set[str] = set(
        _.replace(".egg", "") for _ in import_file.read_text().splitlines()
    )

    # generate requirements file based on installed osparc
    output = subprocess.run(
        [
            "pipdeptree",
            "-p",
            "osparc",
            "--json",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert output.returncode == 0
    dependency_tree: List[Dict[str, Any]] = json.loads(output.stdout)
    dependency_tree = [
        node for node in dependency_tree if node["package"]["key"] == "osparc"
    ]
    assert len(dependency_tree) == 1
    install_dependencies: Set[str] = {
        dep["package_name"].replace("-", "_")
        for dep in dependency_tree[0]["dependencies"]
    }
    msg: str = (
        "imported dependencies not specified "
        f"in setup.py: {import_dependencies - install_dependencies}\n"
        "setup.py dependencies which are "
        f"not imported: {install_dependencies - import_dependencies}"
    )
    assert import_dependencies == install_dependencies, msg


@pytest.mark.parametrize("valid", [True, False])
def test_parent_project_validation(
    faker: Faker, monkeypatch: pytest.MonkeyPatch, valid: bool
):
    if valid:
        monkeypatch.setenv("OSPARC_STUDY_ID", faker.uuid4())
        monkeypatch.setenv("OSPARC_NODE_ID", faker.uuid4())
        parent_info = osparc._settings.ParentProjectInfo()
        assert parent_info.x_simcore_parent_project_uuid is not None
        assert parent_info.x_simcore_parent_node_id is not None
    else:
        monkeypatch.setenv("OSPARC_STUDY_ID", faker.text())
        monkeypatch.setenv("OSPARC_NODE_ID", faker.text())
        with pytest.raises(pydantic.ValidationError):
            _ = osparc._settings.ParentProjectInfo()
