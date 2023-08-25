import asyncio
import json
import math
import random
import shutil
import string
from pathlib import Path
from typing import Any, Iterator, List, Optional, Tuple, Union

import httpx
from httpx import AsyncClient, Response
from osparc_client import (
    BodyCompleteMultipartUploadV0FilesFileIdCompletePost,
    ClientFile,
    ClientFileUploadSchema,
)
from osparc_client import FilesApi as _FilesApi
from osparc_client import FileUploadCompletionBody, FileUploadLinks, UploadedPart
from tqdm.asyncio import tqdm_asyncio

from . import ApiClient, File
from ._http_client import AsyncHttpClient
from ._utils import _file_chunk_generator


class FilesApi(_FilesApi):
    """Class for interacting with files"""

    def __init__(self, api_client: Optional[ApiClient] = None):
        """Construct object

        Args:
            api_client (ApiClient, optinal): osparc.ApiClient object
        """
        super().__init__(api_client)
        self._super = super(FilesApi, self)
        user: Optional[str] = self.api_client.configuration.username
        passwd: Optional[str] = self.api_client.configuration.password
        self._auth: Optional[httpx.BasicAuth] = (
            httpx.BasicAuth(username=user, password=passwd)
            if (user is not None and passwd is not None)
            else None
        )

    def download_file(
        self, file_id: str, *, destination_folder: Optional[Path] = None
    ) -> str:
        if destination_folder is not None and not destination_folder.is_dir():
            raise RuntimeError(
                f"destination_folder: {destination_folder} must be a directory"
            )
        downloaded_file: Path = Path(super().download_file(file_id))
        if destination_folder is not None:
            dest_file: Path = destination_folder / downloaded_file.name
            while dest_file.is_file():
                new_name = (
                    downloaded_file.stem
                    + "".join(random.choices(string.ascii_letters, k=8))
                    + downloaded_file.suffix
                )
                dest_file = destination_folder / new_name
            shutil.move(downloaded_file, dest_file)
            downloaded_file = dest_file
        return str(downloaded_file.resolve())

    def upload_file(self, file: Union[str, Path]):
        return asyncio.run(self.upload_file_async(file=file))

    async def upload_file_async(self, file: Union[str, Path]) -> File:
        if isinstance(file, str):
            file = Path(file)
        if not file.is_file():
            raise RuntimeError(f"{file} is not a file")
        client_file: ClientFile = ClientFile(
            filename=file.name, filesize=file.stat().st_size
        )
        client_upload_schema: ClientFileUploadSchema = self._super.get_upload_links(
            client_file=client_file
        )
        chunk_size: int = client_upload_schema.upload_schema.chunk_size
        links: FileUploadLinks = client_upload_schema.upload_schema.links
        url_iter: Iterator[Tuple[int, str]] = enumerate(
            iter(client_upload_schema.upload_schema.urls), start=1
        )
        if len(client_upload_schema.upload_schema.urls) < math.ceil(
            file.stat().st_size / chunk_size
        ):
            raise RuntimeError(
                "Did not receive sufficient number of upload URLs from the server."
            )

        tasks: list = []
        async with AsyncHttpClient(
            base_url=httpx.URL(self.api_client.configuration.host),
            request_type="post",
            url=links.abort_upload,
            auth=self._auth,
        ) as session:
            async for chunck, size in _file_chunk_generator(file, chunk_size):
                # following https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
                index, url = next(url_iter)
                task = asyncio.create_task(
                    self._upload_chunck(
                        http_client=session,
                        chunck=chunck,
                        chunck_size=size,
                        upload_link=url,
                        index=index,
                    )
                )
                tasks.append(task)

            uploaded_parts: List[UploadedPart] = await tqdm_asyncio.gather(*tasks)

            return await self._complete_multipart_upload(
                session, links.complete_upload, client_file, uploaded_parts
            )

    async def _complete_multipart_upload(
        self,
        http_client: AsyncClient,
        complete_link: str,
        client_file: ClientFile,
        uploaded_parts: List[UploadedPart],
    ) -> File:
        complete_payload = BodyCompleteMultipartUploadV0FilesFileIdCompletePost(
            client_file=client_file,
            uploaded_parts=FileUploadCompletionBody(parts=uploaded_parts),
        )
        response: Response = await http_client.post(
            complete_link,
            json=complete_payload.to_dict(),
            auth=self._auth,
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        return File(**payload)

    async def _upload_chunck(
        self,
        http_client: AsyncClient,
        chunck: bytes,
        chunck_size: int,
        upload_link: str,
        index: int,
    ) -> UploadedPart:
        response: Response = await http_client.put(
            upload_link, content=chunck, headers={"Content-Length": f"{chunck_size}"}
        )
        response.raise_for_status()
        assert response.headers  # nosec
        assert "Etag" in response.headers  # nosec
        etag: str = json.loads(response.headers["Etag"])
        return UploadedPart(number=index, e_tag=etag)
