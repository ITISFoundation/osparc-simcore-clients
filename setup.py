# coding: utf-8

from pathlib import Path

from setuptools import setup, find_packages

NAME = "osparc-simcore-python-api"
VERSION = "0.3.2"
REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]
README = Path("README.md").read_text()

setup(
    name=NAME,
    version=VERSION,
    description="Public API Server",
    author="pcrespov",
    author_email="support@osparc.io",
    url="https://github.com/ITISFoundation/osparc-simcore-python-client.git",
    project_urls={
        "Bug Tracker": "https://github.com/ITISFoundation/osparc-simcore-python-client/issues",
        "Documentation": "https://itisfoundation.github.io/osparc-simcore-python-client",
        "Source Code": "https://github.com/ITISFoundation/osparc-simcore-python-client.git",
    },
    keywords=["OpenAPI", "OpenAPI-Generator", "Public API Server"],
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
