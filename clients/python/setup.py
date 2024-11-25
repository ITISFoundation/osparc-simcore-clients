"""
To install the library, run the following

python setup.py install


prerequisites:
    - setuptools
    - VERSION

SEE http://pypi.python.org/pypi/setuptools
"""

from pathlib import Path

from setuptools import find_packages, setup  # noqa: H301

VERSION_FILE: Path = Path(__file__).parent / "VERSION"
assert VERSION_FILE.is_file(), "Did you forget `make VERSION`?"

NAME = "osparc"
VERSION = VERSION_FILE.read_text().strip()

REQUIRES = [
    "httpx",
    "nest_asyncio",
    "packaging",
    "pydantic-settings",
    "pydantic",
    "tenacity",
    "tqdm>=4.48.0",
    f"osparc_client=={VERSION}",
    "urllib3",
    "aiofiles",
]

SETUP = dict(
    name=NAME,
    version=VERSION,
    description="osparc.io web API",
    author="pcrespov, bisgaard-itis",
    author_email="support@osparc.io",
    url="https://itisfoundation.github.io/osparc-simcore-clients/",
    install_requires=REQUIRES,
    include_package_data=True,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "": [
            "data/openapi.json",
        ]
    },
    long_description=(
        "Please visit our "
        "[website](https://itisfoundation.github.io/osparc-simcore-clients/#/) "
        "for documentation."
    ),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)


if __name__ == "__main__":
    setup(**SETUP)
