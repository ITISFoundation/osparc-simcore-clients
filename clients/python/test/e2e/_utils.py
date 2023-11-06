import os
import subprocess
from pathlib import Path

import osparc
import pytest
from packaging.version import Version

_python_dir: Path = Path(__file__).parent.parent.parent
assert _python_dir.is_dir()


def osparc_dev_features_enabled() -> bool:
    return os.environ.get("OSPARC_DEV_FEATURES_ENABLED") == "1"


def repo_version() -> Version:
    subprocess.run(
        "make client/VERSION", cwd=_python_dir.resolve(), shell=True
    ).check_returncode()
    version_file: Path = Path(_python_dir / "client" / "VERSION")
    assert version_file.is_file()
    return Version(version_file.read_text())


def requires_dev_features(test):
    if (
        Version(osparc.__version__) < repo_version()
        or not osparc_dev_features_enabled()
    ):
        return pytest.mark.skip(
            (
                f"{osparc.__version__=}<{str(repo_version)} "
                "or {osparc_dev_features_enabled()=}"
            )
        )(test)
    return test
