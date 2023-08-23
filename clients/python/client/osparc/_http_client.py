from typing import Optional

import httpx
import tenacity


class AsyncHttpClient:
    """Async http client context manager"""

    def __init__(
        self,
        exc_req_typ: Optional[str] = None,
        exc_url: Optional[str] = None,
        exc_auth: Optional[httpx.BasicAuth] = None,
    ):
        self._client = httpx.AsyncClient()
        self._exc_callback = getattr(self._client, exc_req_typ) if exc_req_typ else None
        self._exc_url = exc_url
        self._exc_auth = exc_auth

    async def __aenter__(self) -> httpx.AsyncClient:
        return self._client

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_value is None:
            await self._client.aclose()
        else:  # exception raised: need to handle
            if self._exc_callback is not None:
                try:
                    async for attempt in tenacity.AsyncRetrying(
                        reraise=True,
                        wait=tenacity.wait_fixed(1),
                        stop=tenacity.stop_after_delay(10),
                        retry=tenacity.retry_if_exception_type(httpx.RequestError),
                    ):
                        with attempt:
                            response = await self._exc_callback(
                                self._exc_url, auth=self._exc_auth
                            )
                            response.raise_for_status()
                except Exception as err:
                    await self._client.aclose()
                    raise err from exc_value
            await self._client.aclose()
            raise exc_value
