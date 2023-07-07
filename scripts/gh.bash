#!/bin/bash

# Github CLI (https://cli.github.com/)
# The Dockerfile for generating the image used here is located here: https://github.com/ITISFoundation/osparc-simcore-clients/blob/master/scripts/gh/Dockerfile
# By default the pwd is mounted into the docker container and used as the current working directory
# Github CLI will need to find the GH_TOKEN environment variable with a valid github token. To espose that to this script, either expose it directly be exporting it,
# or create the file ~/gh-token exporting it.

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

IMAGE_NAME=itisfoundation/gh
IMAGE_VERSION=v0

USERID=$(id -u)
USER_DIR=$(realpath ~)
GH_TOKEN_FILE=${USER_DIR}/.gh-token

if [ -v GITHUB_ACTIONS ]; then
  gh "$@"
else
  if [ ! -f "${GH_TOKEN_FILE}" ] && [ ! -v GH_TOKEN ]; then
      msg="The GH_TOKEN environment variable was not defined and the file '${GH_TOKEN_FILE}' does not exist. To use this script one of them must be present to expose your GH_TOKEN to the docker image. "
      msg+="Either 'export GH_TOKEN=<your github token>' or create the file '${GH_TOKEN_FILE}' and expose your github token in it as follows: "
      msg+="GH_TOKEN=<your github token> "
      echo ${msg}
      exit 1
  fi
  env_file_flag=""
  if [ -f "${GH_TOKEN_FILE}" ]; then
      env_file_flag="--env-file=${GH_TOKEN_FILE}"
  fi
  env_var_flag=""
  if [ -v GH_TOKEN ]; then
      env_var_flag="--env=GH_TOKEN"
  fi
  curdir=/tmp/curdir
  docker run --rm ${env_file_flag} ${env_var_flag} --volume=$(pwd):${curdir} --workdir=${curdir} --user=${USERID}:${USERID}\
    ${IMAGE_NAME}:${IMAGE_VERSION} "$@"
fi
