import json
from pathlib import Path
from typing import Any, Dict

from setuptools import find_packages, setup  # noqa: H301

repo_root: Path = (Path(__file__) / "../../../..").resolve()

config: Dict[str, Any] = json.loads((repo_root / "api/config.json").read_text())

NAME = "osparc"
VERSION = f"{config['python']['version']}"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [f"osparc_client=={VERSION}", "httpx", "tqdm", "nest_asyncio", "tenacity"]

setup(
    name=NAME,
    version=VERSION,
    description="osparc.io web API",
    author="pcrespov, bisgaard-itis",
    author_email="support@osparc.io",
    url="https://itisfoundation.github.io/osparc-simcore-clients/",
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    package_dir={"": "."},
    package_data={
        "": [
            "data/openapi.json",
        ]
    },
    long_description=(
        "Please visit our [website](https://itisfoundation.github.io/osparc-simcore-clients/#/)"
        "for documentation."
    ),
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
