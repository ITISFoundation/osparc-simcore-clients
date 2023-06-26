#!/bin/bash

# Github CLI (https://cli.github.com/)
# First time using this you might be requested to login to github


USER_DIR=$(realpath ~)
GH_CONFIG_DIR=${USER_DIR}/config/gh
source $(dirname "$0")/gh/config.bash

if [[ -n "$GITHUB_ACTIONS" ]]; then
  echo "Running in GitHub Actions"
  gh "$@"
else
  if [ ! -d "${GH_CONFIG_DIR}" ]; then
      mkdir -p "${GH_CONFIG_DIR}"
      echo "Directory created: ${GH_CONFIG_DIR}"
  fi
  docker run --rm --volume="${GH_CONFIG_DIR}":"/root/config/gh" \
    ${IMAGE_NAME}:${IMAGE_VERSION} "$@"
fi
