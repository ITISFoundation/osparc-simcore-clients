#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

source config.bash

docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .
docker push ${IMAGE_NAME}:${IMAGE_VERSION}
