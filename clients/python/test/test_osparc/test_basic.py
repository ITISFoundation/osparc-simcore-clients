import osparc


def test_get_api():
    info = osparc.openapi()
    assert isinstance(info["info"]["version"], str)
