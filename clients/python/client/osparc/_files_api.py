from pathlib import Path
from typing import Optional

from osparc_client import FilesApi as _FilesApi

from . import ApiClient, File


class FilesApi(_FilesApi):
    """Class for interacting with files"""

    def __init__(self, api_client: Optional[ApiClient] = None):
        """Construct object

        Args:
            api_client (ApiClient, optinal): osparc.ApiClient object
        """
        super().__init__(api_client)

    def upload_file(self, file: Path) -> File:
        if not file.is_file():
            raise RuntimeError(f"{file} is not a file")

        return super().upload_file(file)
