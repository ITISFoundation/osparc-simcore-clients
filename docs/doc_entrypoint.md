# osparc

[![PyPI version](https://img.shields.io/pypi/v/osparc)](https://pypi.org/project/osparc/)
[![PyPI - Release](https://img.shields.io/pypi/status/osparc)](https://pypi.org/project/osparc/#history)
[![PyPI Downloads](https://img.shields.io/pypi/dm/osparc)](https://pypi.org/project/osparc/)

`osparc` is a Python package that provides tools and functionalities to interact with the o²S²PARC platform. It allows for seamless integration and automation of workflows in simulation science, making it easier to handle simulations and access [o²S²PARC services](https://github.com/ITISFoundation/osparc-simcore)

## Features

- Interact with the o²S²PARC platform
- Automate workflows and simulations
- Easily manage data and compute resources

## Installation

You can install `osparc` directly from PyPI:

```bash
pip install osparc
```

## Getting Started with `osparc`

### API Key/Secret Setup

Before interacting with the osparc API, you need to generate an API key-secret pair from your osparc account. Follow the [instructions here](https://docs.osparc.io/#/docs/platform_introduction/user_setup/security_details?id=generating-o%c2%b2s%c2%b2parc-tokens) to create the key and secret.

Once generated, you can configure them by either:

1. Setting environment variables:
   - `OSPARC_API_KEY`
   - `OSPARC_API_SECRET`

   Or,

2. Explicitly creating a `osparc.Configuration` instance and passing it to the `osparc.ApiClient`.

### Minimal Example

Here’s a minimal script demonstrating how to interact with the osparc API to retrieve your user profile:

```python
import os
from osparc import ApiClient, UsersApi

# Initialize the API client
with ApiClient() as api_client:
    users_api = UsersApi(api_client)

    # Fetch and print user profile information
    profile = users_api.get_my_profile()
    print(profile)

    # Example output:
    # {'first_name': 'foo',
    #  'gravatar_id': 'aa33fssec77ea434c2ea4fb92d0fd379e',
    #  'groups': {'all': {'description': 'all users',
    #                     'gid': '1',
    #                     'label': 'Everyone'},
    #             'me': {'description': 'primary group',
    #                    'gid': '2',
    #                    'label': 'foo'},
    #             'organizations': []},
    #  'last_name': '',
    #  'login': 'foo@itis.swiss',
    #  'role': 'USER'}
```

## Additional Resources

For more in-depth usage, refer to the following resources:

- 📚 Documentation
  - [Version 0.8](clients/python/docs/v0.8.0/README.md)
  - [Version 0.6](clients/python/docs/v0.6.0/README.md)
  - [Version 0.5](clients/python/docs/v0.5.0/README.md)
- [Community-Contributed Scripts](https://github.com/topics/osparc-python)
  - ✨ [gh:newton1985/osparc_api_example](https://github.com/newton1985/osparc_api_example): A repository containing a "standalone" sample project that illustrates the use of the osparc API
  - ✨ [gh:rwydaegh/goliat](https://github.com/rwydaegh/goliat): Repository for the GOLIAT simulation source code and framework.

>💡 If you want your scripts to be listed here, just create a github repository and [tag it with the  `osparc-python` topic](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).


## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
