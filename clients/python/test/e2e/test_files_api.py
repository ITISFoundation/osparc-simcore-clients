# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import hashlib
from pathlib import Path

import osparc
import pytest
from memory_profiler import memory_usage
from typing import Final, List, Callable
from pydantic import ByteSize
from _utils import skip_if_osparc_version
from packaging.version import Version

_KB: ByteSize = ByteSize(1024)  # in bytes
_MB: ByteSize = ByteSize(_KB * 1024)  # in bytes
_GB: ByteSize = ByteSize(_MB * 1024)  # in bytes


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


def test_upload_file(
    create_tmp_file: Callable[[ByteSize], Path], api_client: osparc.ApiClient
) -> None:
    """Test that we can upload a file via the multipart upload and download it again."""
    tmp_file = create_tmp_file(ByteSize(1 * _GB))
    tmp_path: Path = tmp_file.parent
    files_api: osparc.FilesApi = osparc.FilesApi(api_client=api_client)
    try:
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
    finally:
        files_api.delete_file(uploaded_file1.id)


@skip_if_osparc_version(at_least=Version("0.8.3.post0.dev12"))
def test_upload_download_file_ram_usage(
    create_tmp_file: Callable[[ByteSize], Path], api_client: osparc.ApiClient
) -> None:
    """Check RAM usage of upload/download fcns"""
    _allowed_ram_usage_in_mb: Final[int] = 300  # 300MB
    tmp_file = create_tmp_file(ByteSize(1 * _GB))
    assert (
        tmp_file.stat().st_size > _allowed_ram_usage_in_mb * 1024 * 1024
    ), "For this test to make sense, file size must be larger than allowed ram usage."

    def max_diff(data: List[int]) -> int:
        return max(data) - min(data)

    tmp_path: Path = tmp_file.parent
    files_api: osparc.FilesApi = osparc.FilesApi(api_client=api_client)
    try:
        upload_ram_usage_in_mb, uploaded_file1 = memory_usage(
            (files_api.upload_file, (tmp_file,)),  # type: ignore
            retval=True,
        )
        assert (
            max_diff(upload_ram_usage_in_mb) < _allowed_ram_usage_in_mb
        ), f"Used more than {_allowed_ram_usage_in_mb=} to upload file of size {tmp_file.stat().st_size=}"
        download_ram_usage_in_mb, downloaded_file = memory_usage(
            (
                files_api.download_file,
                (uploaded_file1.id,),
                {"destination_folder": tmp_path},
            ),  # type: ignore
            retval=True,
        )
        assert (
            max_diff(download_ram_usage_in_mb) < _allowed_ram_usage_in_mb
        ), f"Used more than {_allowed_ram_usage_in_mb=} to download file of size {Path(downloaded_file).stat().st_size=}"
        assert _hash_file(Path(downloaded_file)) == _hash_file(tmp_file)
    finally:
        files_api.delete_file(uploaded_file1.id)


@pytest.mark.parametrize("use_checksum", [True, False])
@pytest.mark.parametrize("use_id", [True, False])
def test_search_files(
    create_tmp_file: Callable[[ByteSize], Path],
    api_client: osparc.ApiClient,
    use_checksum: bool,
    use_id: bool,
) -> None:
    tmp_file = create_tmp_file(ByteSize(1 * _GB))
    checksum: str = _hash_file(tmp_file)
    results: osparc.PaginationGenerator
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
        assert len(results) == 0, "Could find file on server after it had been deleted"

    except Exception:
        # clean up in case of failure
        results = files_api._search_files(sha256_checksum=checksum)
        for file in results:
            files_api.delete_file(file.id)
