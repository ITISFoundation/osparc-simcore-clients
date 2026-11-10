#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

# the image is built from this directory, whatever the caller's working directory is
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

IMAGE_NAME="itisfoundation/osparc_python_tutorial_testing"
# Publish a new tag, never republish one in place: the e2e-portal GitLab CI pins an exact tag
# (`PYTHON_CLIENT_E2E_IMAGE` in its `.gitlab-ci.yml`), so the order is bump here, publish,
# then bump the pin there. Published tags:
#   v1 py3.9 without uv, v2 py3.9 + uv, v3 py3.11 on bookworm, v4 py3.11 on Debian trixie.
IMAGE_VERSION="v4"

docker build --tag "${IMAGE_NAME}:${IMAGE_VERSION}" .
docker push "${IMAGE_NAME}:${IMAGE_VERSION}"
