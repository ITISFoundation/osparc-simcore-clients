from typing import Optional

import httpx
import tenacity


class AsyncHttpClient:
    """Async http client context manager"""

    def __init__(
        self,
        *,
        base_url: httpx.URL,
        request_type: Optional[str] = None,
        url: Optional[str] = None,
        auth: Optional[httpx.BasicAuth] = None,
    ):
        self._client = httpx.AsyncClient(
            base_url=base_url, auth=auth, follow_redirects=True
        )
        self._callback = getattr(self._client, request_type) if request_type else None
        self._url = url

    async def __aenter__(self) -> httpx.AsyncClient:
        return self._client

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        if exc_value is None:
            await self._client.aclose()
        else:  # exception raised: need to handle
            if self._callback is not None:
                try:
                    async for attempt in tenacity.AsyncRetrying(
                        reraise=True,
                        wait=tenacity.wait_fixed(1),
                        stop=tenacity.stop_after_delay(10),
                        retry=tenacity.retry_if_exception_type(httpx.RequestError),
                    ):
                        with attempt:
                            response = await self._callback(self._url)
                            response.raise_for_status()
                except Exception as err:
                    await self._client.aclose()
                    raise err from exc_value
            await self._client.aclose()
            raise exc_value
