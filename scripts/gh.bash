#!/bin/bash

# Github CLI (https://cli.github.com/)
# First time using this you might be requested to login to github


USER_DIR=$(realpath ~)

source $(dirname "$0")/gh/config.bash

if [[ -n "$GITHUB_ACTIONS" ]]; then
  echo "Running in GitHub Actions"
  gh "$@"
else
  docker run --rm --volume="${USER_DIR}/config/gh":"/root/config/gh" \
    ${IMAGE_NAME}:${IMAGE_VERSION} "$@"
fi
