#!/bin/bash

source $(dirname "$0")/jq/config.bash

echo "IMAGE_NAME: ${IMAGE_NAME}"
echo "IMAGE_VERSION: ${IMAGE_VERSION}"
docker run --rm -t ${IMAGE_NAME}:${IMAGE_VERSION} "$@"
