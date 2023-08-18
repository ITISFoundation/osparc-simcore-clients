import asyncio
import json
import math
from pathlib import Path
from typing import Any, Iterator, List, Optional, Tuple, Union

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
from ._warnings_and_errors import aiohttp_error_handler_async


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

    def upload_file(self, file: Union[str, Path]):
        return asyncio.run(self.upload_file_async(file=file))

    @aiohttp_error_handler_async
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
        async with HttpClient(
            exc_req_typ="post", exc_url=links.abort_upload, exc_auth=self._auth
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
        http_client: ClientSession,
        complete_link: str,
        client_file: ClientFile,
        uploaded_parts: List[UploadedPart],
    ) -> File:
        complete_payload = BodyCompleteMultipartUploadV0FilesFileIdCompletePost(
            client_file=client_file,
            uploaded_parts=FileUploadCompletionBody(parts=uploaded_parts),
        )
        async with http_client.post(
            complete_link,
            json=complete_payload.to_dict(),
            auth=self._auth,
        ) as response:
            response.raise_for_status()
            payload: dict[str, Any] = await response.json()
        return File(**payload)

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
