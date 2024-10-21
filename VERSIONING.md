# Versioning Strategy

- We follow **post-release versioning** during development.
  - Format: `1.2.3.post0.devN` where `N` represents the number of commits since the last release (`1.2.3`).
  - We opt for post-release versioning rather than pre-release to avoid making early decisions about the next release version.

- Official releases follow the format `1.2.3`.

- **Patch releases** (e.g., `1.2.4`) are used instead of post-releases like `1.2.3.postX`.

- Releases are determined by **git tags**. SEE [Releases](https://github.com/ITISFoundation/osparc-simcore-clients/releases).

- For more details, refer to the following:
  - GitHub workflow for publishing: `.github/workflows/publish-python-client.yml`
  - Version computation script: `scripts/compute_version.bash`
