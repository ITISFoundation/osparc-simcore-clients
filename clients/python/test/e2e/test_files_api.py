from pathlib import Path

import osparc


def test_upload_file(tmp_path: Path, cfg: osparc.Configuration) -> None:
    """Test that we can upload a file via the multipart upload"""
    # create file to upload
    byte_size: int = 10 * 1024 * 1024 * 1024  # 10 gigabyte
    tmp_file = tmp_path / "large_test_file.txt"
    tmp_file.write_bytes(b"large test file")
    with open(tmp_file, "wb") as f:
        f.truncate(byte_size)
    assert (
        tmp_file.stat().st_size == byte_size
    ), f"Could not create file of size: {byte_size}"

    with osparc.ApiClient(cfg) as api_client:
        files_api: osparc.FilesApi = osparc.FilesApi(api_client=api_client)
        files_api.upload_file(tmp_file)
