import os
import subprocess
from pathlib import Path
from typing import Optional

import osparc
import pytest
from packaging.version import Version

_clients_python_dir: Path = Path(__file__).parent.parent.parent
assert _clients_python_dir.is_dir()


def osparc_dev_features_enabled() -> bool:
    return os.environ.get("OSPARC_DEV_FEATURES_ENABLED") == "1"


def repo_version() -> Version:
    subprocess.run(
        "make VERSION", cwd=_clients_python_dir.resolve(), shell=True
    ).check_returncode()
    version_file: Path = Path(_clients_python_dir / "VERSION")
    assert version_file.is_file()
    return Version(version_file.read_text())


def skip_if_osparc_version(
    *,
    at_least: Optional[Version] = None,
    at_most: Optional[Version] = None,
    exactly: Optional[Version] = None,
):
    def _wrapper(test):
        osparc_version = Version(osparc.__version__)
        if at_least and osparc_version < at_least:
            return pytest.mark.skip((f"{osparc_version=}<{at_least}"))(test)
        if at_most and osparc_version > at_most:
            return pytest.mark.skip((f"{osparc_version=}>{at_most}"))(test)
        if exactly and osparc_version != exactly:
            return pytest.mark.skip((f"{osparc_version=}!={exactly}"))(test)
        return test

    return _wrapper
