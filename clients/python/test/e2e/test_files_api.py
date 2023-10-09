import hashlib
from pathlib import Path

import osparc
import pytest
from _utils import requires_dev_features
from conftest import _KB


def _hash_file(file: Path) -> str:
    assert file.is_file()
    sha256 = hashlib.sha256()
    with open(file, "rb") as f:
        while True:
            data = f.read(100 * _KB)
            if not data:
                break
            sha256.update(data)
        return sha256.hexdigest()


@requires_dev_features
def test_upload_file(tmp_file: Path, cfg: osparc.Configuration) -> None:
    """Test that we can upload a file via the multipart upload"""
    tmp_path: Path = tmp_file.parent
    with osparc.ApiClient(cfg) as api_client:
        files_api: osparc.FilesApi = osparc.FilesApi(api_client=api_client)
        uploaded_file1: osparc.File = files_api.upload_file(tmp_file)
        uploaded_file2: osparc.File = files_api.upload_file(tmp_file)
        assert (
            uploaded_file1.id == uploaded_file2.id
        ), "could not detect that file was already on server"
        downloaded_file = files_api.download_file(
            uploaded_file1.id, destination_folder=tmp_path
        )
        assert Path(downloaded_file).parent == tmp_path
        assert _hash_file(Path(downloaded_file)) == _hash_file(tmp_file)
        files_api.delete_file(uploaded_file1.id)


@requires_dev_features
@pytest.mark.parametrize("use_checksum", [True, False])
@pytest.mark.parametrize("use_id", [True, False])
def test_search_files(
    tmp_file: Path, cfg: osparc.Configuration, use_checksum: bool, use_id: bool
) -> None:
    checksum: str = _hash_file(tmp_file)
    results: osparc.PaginationGenerator
    with osparc.ApiClient(configuration=cfg) as api_client:
        files_api: osparc.FilesApi = osparc.FilesApi(api_client=api_client)
        try:
            results = files_api._search_files(sha256_checksum=checksum)
            assert len(results) == 0, "Found file which shouldn't be there"

            uploaded_file: osparc.File = files_api.upload_file(tmp_file)
            assert checksum == uploaded_file.checksum

            results = files_api._search_files(
                file_id=uploaded_file.id if use_id else None,
                sha256_checksum=uploaded_file.checksum if use_checksum else None,
            )
            assert len(results) == 1, "Could not find file after it had been uploaded"

            files_api.delete_file(uploaded_file.id)
            results = files_api._search_files(
                file_id=uploaded_file.id if use_id else None,
                sha256_checksum=uploaded_file.checksum if use_checksum else None,
            )
            assert (
                len(results) == 0
            ), "Could find file on server after it had been deleted"

        except Exception:
            # clean up in case of failure
            results = files_api._search_files(sha256_checksum=checksum)
            for file in results:
                files_api.delete_file(file.id)
