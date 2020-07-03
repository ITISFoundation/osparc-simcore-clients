# Python client for osparc-simcore API

![test](https://github.com/ITISFoundation/osparc-simcore-python-client/workflows/test/badge.svg)
<!--
TODO: activate when service is up and running in production
[![codecov](https://codecov.io/gh/ITISFoundation/osparc-simcore-python-client/branch/master/graph/badge.svg)](https://codecov.io/gh/ITISFoundation/osparc-simcore-python-client) -->


Python client for osparc-simcore Public RESTful API

- API version: 0.3.0
- Package version: 0.3.2
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements

Python 3.6+

## Installation & Usage

Install the latest release with

```sh
pip install osparc-simcore-python-api
```
or directly from the repository
```sh
pip install git+https://github.com/ITISFoundation/osparc-simcore-python-client.git
```

Then import the package:

```python
import osparc
```

## Getting Started

Please follow the installation procedure above and then run the following:

```python
from __future__ import print_function
import time
import osparc
from osparc.rest import ApiException
from pprint import pprint


# Defining host is optional and default to http://localhost
configuration.host = "http://localhost"

# Enter a context with an instance of the API client
with osparc.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = osparc.MetaApi(api_client)

    try:
        # Get Service Metadata
        api_response = api_instance.get_service_metadata()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling MetaApi->get_service_metadata: %s\n" % e)

```

## Author

Made with love at [Zurich43](www.z43.swiss)