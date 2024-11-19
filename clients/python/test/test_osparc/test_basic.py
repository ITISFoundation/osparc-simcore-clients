import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Set, cast

import osparc
import osparc._settings
import pydantic
import pytest
import respx
from faker import Faker
import httpx
from urllib.parse import urlparse
from osparc._utils import PaginationIterable
from functools import partial
from copy import deepcopy

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
def test_parent_project_validation(faker, valid: bool):
    if valid:
        os.environ["OSPARC_STUDY_ID"] = f"{faker.uuid4()}"
        os.environ["OSPARC_NODE_ID"] = f"{faker.uuid4()}"
        parent_info = osparc._settings.ParentProjectInfo()
        assert parent_info.x_simcore_parent_project_uuid is not None
        assert parent_info.x_simcore_parent_node_id is not None
    else:
        os.environ["OSPARC_STUDY_ID"] = f"{faker.text()}"
        os.environ["OSPARC_NODE_ID"] = f"{faker.text()}"
        with pytest.raises(pydantic.ValidationError):
            _ = osparc._settings.ParentProjectInfo()


def test_pagination_iterator(
    faker: Faker, page_file: osparc.PageFile, api_client: osparc.ApiClient
):
    next_page_url = urlparse(page_file.links.next)
    _base_url = f"{next_page_url.scheme}://{next_page_url.netloc}"
    _auth = httpx.BasicAuth(
        username=api_client.configuration.username,
        password=api_client.configuration.password,
    )

    def _sideeffect(all_items: List, request: httpx.Request):
        n_remaining_items = cast(int, page_file.total) - len(all_items)
        assert n_remaining_items >= 0
        if len(page_file.items) >= n_remaining_items:
            page_file.items = page_file.items[:n_remaining_items]
            page_file.links.next = None
        all_items += page_file.items
        return httpx.Response(status_code=200, json=page_file.to_dict())

    with respx.mock(
        base_url=_base_url,
        assert_all_called=True,
    ) as respx_mock:
        server_items: List[osparc.File] = deepcopy(page_file.items)
        respx_mock.get(urlparse(page_file.links.next).path).mock(
            side_effect=partial(_sideeffect, server_items)
        )

        pagination_iterator = PaginationIterable(
            lambda: page_file, api_client=api_client, base_url=_base_url, auth=_auth
        )
        client_items = [item for item in pagination_iterator]
        assert len(server_items) > 0
        assert server_items == client_items

        first_client_item = next(iter(pagination_iterator))
        assert first_client_item == server_items[0]

        assert len(pagination_iterator) == page_file.total
