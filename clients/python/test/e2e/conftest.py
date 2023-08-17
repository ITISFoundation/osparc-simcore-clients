import os

import osparc
import pytest


@pytest.fixture
def cfg() -> osparc.Configuration:
    """Configuration

    Returns:
        osparc.Configuration: The Configuration
    """
    cfg = osparc.Configuration(
        host=os.environ["OSPARC_API_HOST"],
        username=os.environ["OSPARC_API_KEY"],
        password=os.environ["OSPARC_API_SECRET"],
    )
    return cfg
