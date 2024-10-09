# Releases

Some notes on how the clients are version and released

## openapi specs (OAS) version != client version

The version found in api/openapi.json for the API is **not used** as the version of the client.

## Versioning Strategy

- We follow **post-release versioning** during development.
  - Format: `1.2.3.post0.devN` where `N` represents the number of commits since the last release (`1.2.3`).
  - We opt for post-release versioning rather than pre-release to avoid making early decisions about the next release version.

- Official releases follow the format `1.2.3`.

- **Patch releases** (e.g., `1.2.4`) are used instead of post-releases like `1.2.3.postX`.

- Releases are determined by **git tags**. SEE [Releases](https://github.com/ITISFoundation/osparc-simcore-clients/releases).

- For more details, refer to the following:
  - GitHub workflow for publishing: `.github/workflows/publish-python-client.yml`
  - Version computation script: `scripts/compute_version.bash`


## `osparc` Package in the https://pypi.org Package Index

- Release history in https://pypi.org/project/osparc/#history
  - Corresponds to [Releases](https://github.com/ITISFoundation/osparc-simcore-clients/releases).
- Pre-releases in https://test.pypi.org/project/osparc/#history
  - all master commits have a pre-released as `X.Y.Z.post0.devN`

### FAQ

#### How to install latest released versions?

```cmd
pip install osparc
```

#### How to list all released versions?

```cmd
pip index versions osparc
```

#### How to list pre-released versions?

For that we need to include the test index, where we decided to push all the pre-releases. An extra
index to the standard pypi repo is necessary in order to find the dependencies

```cmd
pip index versions osparc -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --pre
```

#### How to install latest pre-release versions?

```cmd
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ osparc
```
