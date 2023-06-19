# coding: utf-8

from pathlib import Path

from setuptools import setup, find_packages

NAME = "osparc"
VERSION = "0.5.0"
API_VERSION = "0.4.0"
REQUIRES = ["urllib3 >= 1.26.4", "six >= 1.10", "certifi", "python-dateutil"]
README = (Path(__file__).parent / 'README.md').read_text()

setup(
    name=NAME,
    version=VERSION,
    description=f"python client for osparc web API v{API_VERSION}",
    author="pcrespov",
    author_email="support@osparc.io",
    url="https://github.com/ITISFoundation/osparc-simcore-clients.git",
    project_urls={
        "Bug Tracker": "https://github.com/ITISFoundation/osparc-simcore-clients/issues",
        "Documentation": "https://itisfoundation.github.io/osparc-simcore-clients",
        "Source Code": "https://github.com/ITISFoundation/osparc-simcore-clients.git",
    },
    keywords=["OpenAPI", "OpenAPI-Generator", "osparc", "web API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description=README,
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
