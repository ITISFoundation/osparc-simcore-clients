
import osparc

def test_osparc_client():
    from osparc import osparc_client

def test_get_api():
    info = osparc.info.openapi()
    assert isinstance(info['info']['version'],str)
