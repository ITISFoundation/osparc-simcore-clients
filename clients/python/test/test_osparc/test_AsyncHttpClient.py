import httpx
import osparc
import pytest
import respx
from osparc._http_client import AsyncHttpClient


@pytest.fixture
def fake_retry_state():
    def _(r: httpx.Response):
        class Exc:
            response = r

        class Outcome:
            def exception(self):
                return Exc()

        class FakeRetryCallState:
            outcome = Outcome()

        return FakeRetryCallState()

    yield _


def test_retry_strategy(cfg: osparc.Configuration, fake_retry_state):
    async_client = AsyncHttpClient(
        configuration=cfg,
        request_type="get",
        url="79ae41cc-0d89-4714-ac9d-c23ee1b110ce",
    )
    assert (
        async_client._wait_callback(
            fake_retry_state(
                httpx.Response(
                    status_code=503,
                    headers={"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"},
                )
            )
        )
        < 0
    )
    assert (
        async_client._wait_callback(
            fake_retry_state(
                httpx.Response(
                    status_code=503,
                    headers={"Retry-After": "15"},
                )
            )
        )
        == 15
    )


async def test_aexit(cfg: osparc.Configuration, respx_mock: respx.Mock):
    _call_url: str = "5b0c5cb6-5e88-479c-a54d-2d5fa39aa97b"
    _exit_url: str = "43c2fdfc-690e-4ba9-9ae7-55a911c159d0"

    def _side_effect(status_code: int, request: httpx.Request):
        return httpx.Response(status_code=status_code)

    respx_mock.get(_call_url).mock(side_effect=_side_effect)

    async with AsyncHttpClient(
        configuration=cfg,
        request_type="get",
        url="79ae41cc-0d89-4714-ac9d-c23ee1b110ce",
        body={"this": "field"},
    ):
        pass
