# pylint: disable=protected-access
# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
# pylint: disable=unused-variable

import hashlib
from pathlib import Path

import osparc
from osparc._utils import PaginationIterable
import pytest
from memory_profiler import memory_usage
from typing import Final, Callable
from pydantic import ByteSize
from _utils import skip_if_osparc_version
from packaging.version import Version
from conftest import ServerFile, _KB
from faker import Faker


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


@skip_if_osparc_version(at_least=Version("0.8.0"), at_most=Version("0.8.3.post0.dev11"))
def test_upload_file(
    tmp_path: Path, large_server_file: ServerFile, files_api: osparc.FilesApi
) -> None:
    """Test that we can upload a file via the multipart upload and download it again."""
    uploaded_file: osparc.File = files_api.upload_file(large_server_file.local_file)
    assert (
        large_server_file.server_file.id == uploaded_file.id
    ), "could not detect that file was already on server"
    downloaded_file = files_api.download_file(
        uploaded_file.id, destination_folder=tmp_path
    )
    assert Path(downloaded_file).parent == tmp_path
    assert _hash_file(Path(downloaded_file)) == _hash_file(large_server_file.local_file)


@skip_if_osparc_version(at_least=Version("0.8.3.post0.dev12"))
def test_upload_download_file_ram_usage(
    tmp_path: Path, large_server_file: ServerFile, files_api: osparc.FilesApi
) -> None:
    """Check RAM usage of upload/download fcns"""
    _allowed_ram_usage_in_mb: Final[int] = 300  # 300MB
    assert (
        large_server_file.local_file.stat().st_size
        > _allowed_ram_usage_in_mb * 1024 * 1024
    ), f"For this test to make sense, {large_server_file.local_file.stat().st_size=} must be larger than {_allowed_ram_usage_in_mb=}."

    uploaded_file = files_api.upload_file(large_server_file.local_file)
    assert (
        large_server_file.server_file.id == uploaded_file.id
    ), "could not detect that file was already on server"

    download_ram_usage_in_mb, downloaded_file = memory_usage(
        (
            files_api.download_file,
            (uploaded_file.id,),
            {"destination_folder": tmp_path},
        ),  # type: ignore
        retval=True,
    )
    assert Path(downloaded_file).parent == tmp_path
    assert (
        max(download_ram_usage_in_mb) - min(download_ram_usage_in_mb)
        < _allowed_ram_usage_in_mb
    ), f"Used more than {_allowed_ram_usage_in_mb=} to download file of size {Path(downloaded_file).stat().st_size=}"
    assert _hash_file(Path(downloaded_file)) == _hash_file(large_server_file.local_file)


@skip_if_osparc_version(at_least=Version("0.8.3.post0.dev20"))
@pytest.mark.parametrize(
    "use_checksum,use_id", [(True, True), (False, True), (True, False)]
)
def test_search_files(
    large_server_file: Callable[[ByteSize], Path],
    files_api: osparc.FilesApi,
    use_checksum: bool,
    use_id: bool,
    faker: Faker,
) -> None:
    results: PaginationIterable = files_api._search_files(
        sha256_checksum=f"{faker.sha256()}"
    )
    assert len(results) == 0, "Found file which shouldn't be there"

    results = files_api._search_files(
        file_id=large_server_file.server_file.id if use_id else None,
        sha256_checksum=large_server_file.server_file.checksum
        if use_checksum
        else None,
    )
    assert len(results) == 1, "Could not find file after it had been uploaded"
    file = next(iter(results))
    assert file.checksum == large_server_file.server_file.checksum
