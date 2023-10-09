import json
import os
from pathlib import Path

import osparc
import pytest
from packaging.version import Version

_config: Path = (
    Path(__file__).parent.parent.parent.parent.parent / "api" / "config.json"
)
assert _config.is_file()


def osparc_dev_features_enabled() -> bool:
    return os.environ.get("OSPARC_DEV_FEATURES_ENABLED") == "1"


def requires_dev_features(test):
    repo_version: Version = Version(
        json.loads(_config.read_text())["python"]["version"]
    )
    if Version(osparc.__version__) < repo_version or not osparc_dev_features_enabled():
        return pytest.mark.skip(
            (
                f"{osparc.__version__=}<{str(repo_version)} "
                "or {osparc_dev_features_enabled()=}"
            )
        )(test)
    return test
