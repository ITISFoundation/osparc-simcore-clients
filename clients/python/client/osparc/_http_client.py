from aiohttp import ClientSession


class HttpClient:
    """Async http client context manager"""

    def __init__(self):
        self._client = ClientSession()

    async def __aenter__(self) -> ClientSession:
        return self._client

    async def __aexit__(self) -> None:
        await self._client.close()
        return
