#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

# the image is built from this directory, whatever the caller's working directory is
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

IMAGE_NAME="itisfoundation/osparc_python_tutorial_testing"
# NOTE: publish new tags, never republish v1 in place: the e2e-portal GitLab CI
# pins itisfoundation/osparc_python_tutorial_testing:v1 and must keep working.
IMAGE_VERSION="v3"

docker build --tag "${IMAGE_NAME}:${IMAGE_VERSION}" .
docker push "${IMAGE_NAME}:${IMAGE_VERSION}"
