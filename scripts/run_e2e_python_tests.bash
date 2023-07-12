#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

ROOT_DIR=$(realpath "$(dirname "$0")/..")
SCRIPTS_DIR=${ROOT_DIR}/scripts
PYTHON_DIR=${ROOT_DIR}/clients/python


unset CLIENT_REPO
unset CLIENT_BRANCH
unset CLIENT_VERSION
unset SERVER_CONFIG

while getopts ":c:s:" arg; do
  case $arg in
    c) # Define client configuration
      ARG="${OPTARG}"
      CLIENT_REPO=$(echo "${ARG}" | jq .CLIENT_REPO)
      CLIENT_BRANCH=$(echo "${ARG}" | jq .CLIENT_BRANCH)
      CLIENT_VERSION=$(echo "${ARG}" | jq .CLIENT_VERSION)
      echo "Received CLIENT_REPO=${CLIENT_REPO}, CLIENT_BRANCH=${CLIENT_BRANCH}, CLIENT_VERSION=${CLIENT_VERSION}"
      ;;
    s)
      SERVER_CONFIG="${OPTARG}"
      ;;
    *)
      echo "Received unknown flag"
      exit 1
      ;;
  esac
done

#bash "${SCRIPTS_DIR}"/install_ci_osparc_python_client.bash -r "${CLIENT_REPO}" -b "${CLIENT_BRANCH}" -v "${CLIENT_VERSION}"
for server in $(echo "${SERVER_CONFIG}" | jq keys[])
do
    key=$(echo "${SERVER_CONFIG}" | jq ".${server}.key")
    secret=$(echo "${SERVER_CONFIG}" | jq ".${server}.secret")
    python "${PYTHON_DIR}"/test/e2e/setup_e2e_config.py "${server}" "${key}" "${secret}" "${CLIENT_REPO}" "${CLIENT_BRANCH}" "${CLIENT_VERSION}"
    pytest "${PYTHON_DIR}"/test/e2e
done
