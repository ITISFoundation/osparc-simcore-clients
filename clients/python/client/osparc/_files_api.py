import asyncio
import json
import math
from pathlib import Path
from typing import Any, Iterator, Optional

import aiohttp
from aiohttp import ClientSession
from osparc_client import (
    BodyCompleteMultipartUploadV0FilesFileIdCompletePost,
    ClientFile,
    ClientFileUploadSchema,
)
from osparc_client import FilesApi as _FilesApi
from osparc_client import FileUploadCompletionBody, FileUploadLinks, UploadedPart
from tqdm.asyncio import tqdm_asyncio

from . import ApiClient, File
from ._http_client import HttpClient
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
        self._auth: aiohttp.BasicAuth = aiohttp.BasicAuth(
            login=self.api_client.configuration.username,
            password=self.api_client.configuration.password,
        )

    def upload_file(self, file):
        return asyncio.run(self.upload_file_async(file=file))

    async def upload_file_async(self, file: Path) -> File:
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
        url_iter: Iterator[str] = iter(client_upload_schema.upload_schema.urls)
        if len(client_upload_schema.upload_schema.urls) < math.ceil(
            file.stat().st_size / chunk_size
        ):
            raise RuntimeError(
                "Did not receive sufficient number of upload URLs from the server."
            )

        tasks: list = []
        index: int = 1
        async with HttpClient() as session:
            try:
                async for chunck, size in _file_chunk_generator(file, chunk_size):
                    # following https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
                    task = asyncio.create_task(
                        self._upload_chunck(
                            http_client=session,
                            chunck=chunck,
                            chunck_size=size,
                            upload_link=next(url_iter),
                            index=index,
                        )
                    )
                    tasks.append(task)
                    index += 1

                uploaded_parts: list[UploadedPart] = await tqdm_asyncio.gather(*tasks)

                complete_payload = BodyCompleteMultipartUploadV0FilesFileIdCompletePost(
                    client_file=client_file,
                    uploaded_parts=FileUploadCompletionBody(parts=uploaded_parts),
                )
                async with session.post(
                    links.complete_upload,
                    json=complete_payload.to_dict(),
                    auth=self._auth,
                ) as response:
                    response.raise_for_status()
                    payload: dict[str, Any] = await response.json()
                    server_file = File(**payload)

            except Exception as e:
                async with session.post(
                    links.abort_upload, auth=self._auth
                ) as response:
                    response.raise_for_status()
                raise e

        return server_file

    async def _upload_chunck(
        self,
        http_client: ClientSession,
        chunck: bytes,
        chunck_size: int,
        upload_link: str,
        index: int,
    ) -> UploadedPart:
        async with http_client.put(
            upload_link, data=chunck, headers={"Content-Length": f"{chunck_size}"}
        ) as response:
            response.raise_for_status()
            assert response.headers  # nosec
            assert "Etag" in response.headers  # nosec
            etag: str = json.loads(response.headers["Etag"])
            return UploadedPart(number=index, e_tag=etag)
