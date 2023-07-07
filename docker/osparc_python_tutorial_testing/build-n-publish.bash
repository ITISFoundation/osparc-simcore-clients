#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

IMAGE_NAME="itisfoundation/osparc_python_tutorial_testing"
IMAGE_VERSION="v0"

docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .
docker push ${IMAGE_NAME}:${IMAGE_VERSION}
