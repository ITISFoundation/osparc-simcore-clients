import json

import httpx
import osparc
import pytest
import respx
from faker import Faker
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
        method="get",
        url="79ae41cc-0d89-4714-ac9d-c23ee1b110ce",
        body={},
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


async def test_aexit(
    cfg: osparc.Configuration, respx_mock: respx.MockRouter, faker: Faker
):
    _call_url: str = "https://5b0c5cb6-5e88-479c-a54d-2d5fa39aa97b"
    _exit_url: str = "https://43c2fdfc-690e-4ba9-9ae7-55a911c159d0"
    _body = {"msg": faker.text()}

    def _side_effect(request: httpx.Request):
        msg = json.loads(request.content.decode()).get("msg")
        assert msg
        assert _body["msg"] == msg
        return httpx.Response(status_code=200)

    exit_mock = respx_mock.post(_exit_url).mock(side_effect=_side_effect)
    respx_mock.put(_call_url).mock(return_value=httpx.Response(500))

    with pytest.raises(httpx.HTTPError):
        async with AsyncHttpClient(
            configuration=cfg,
            method="post",
            url=_exit_url,
            body=_body,
        ) as session:
            response = await session.put(_call_url)
            response.raise_for_status()

    assert exit_mock.called
