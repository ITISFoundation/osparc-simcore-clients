from setuptools import setup, find_packages  # noqa: H301
from pathlib import Path
import json
from typing import Any

repo_root: Path = (Path(__file__) / '../../../..').resolve()

config: dict[str: Any] = json.loads((repo_root / 'api/config.json').read_text())

NAME = "osparc"
VERSION = f"{config['python']['version']}"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [f"osparc_raw == {VERSION}"]

setup(
    name=NAME,
    version=VERSION,
    description="osparc.io web API",
    author="pcrespov, bisgaard-itis",
    author_email="support@osparc.io",
    url="",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    data_files=[('meta',[str('../../../../api/openapi.json')])],
    long_description="osparc client",
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
