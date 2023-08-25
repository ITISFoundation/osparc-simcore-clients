import hashlib
from pathlib import Path

import osparc
import pytest
from packaging.version import Version

_KB = 1024  # in bytes
_MB = _KB * 1024  # in bytes
_GB = _MB * 1024  # in bytes


def _hash_file(file: Path) -> str:
    assert file.is_file()
    md5 = hashlib.md5()
    with open(file, "rb") as f:
        while True:
            data = f.read(100 * _KB)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()


# @pytest.mark.skip(reason="Skipped until files_api.delete_file() is implemented")
@pytest.mark.skipif(
    Version(osparc.__version__) < Version("0.6.0"),
    reason=f"osparc.__version__={osparc.__version__} is older than 0.6.0",
)
def test_upload_file(tmp_path: Path, cfg: osparc.Configuration) -> None:
    """Test that we can upload a file via the multipart upload"""
    # create file to upload
    byte_size: int = 1 * _GB
    tmp_file = tmp_path / "large_test_file.txt"
    tmp_file.write_bytes(b"large test file")
    with open(tmp_file, "wb") as f:
        f.truncate(byte_size)
    assert (
        tmp_file.stat().st_size == byte_size
    ), f"Could not create file of size: {byte_size}"

    with osparc.ApiClient(cfg) as api_client:
        files_api: osparc.FilesApi = osparc.FilesApi(api_client=api_client)
        uploaded_file: osparc.File = files_api.upload_file(tmp_file)
        downloaded_file = files_api.download_file(
            uploaded_file.id, destination_folder=tmp_path
        )
        assert Path(downloaded_file).parent == tmp_path
        assert _hash_file(Path(downloaded_file)) == _hash_file(tmp_file)
        files_api.delete_file(uploaded_file.id)
