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

## Usage

To get started with `osparc`, import the package and follow the examples in the [documentation](https://github.com/your-username/osparc/wiki).


```python
from osparc import ApiClient, UsersApi

cfg = Configuration(
    host=os.environ["OSPARC_API_HOST"],
    username=os.environ["OSPARC_API_KEY"],
    password=os.environ["OSPARC_API_SECRET"],
)

with ApiClient(cfg) as api_client:

    users_api = UsersApi(api_client)

    profile = users_api.get_my_profile()
    print(profile)

    #
    #  {'first_name': 'foo',
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
    #
```
To dive deeper check these tutorials
  - [v0.5](clients/python/docs/v0.5.0/README.md)
  - [v0.6](clients/python/docs/v0.6.0/README.md)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get involved.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

---

Make sure to replace `your-username` with your actual GitHub username or repository link, and feel free to modify the sections as necessary.
