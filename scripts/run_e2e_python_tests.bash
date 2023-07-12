#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

ROOT_DIR=$(realpath "$(dirname "$0")/..")
PYTHON_DIR=${ROOT_DIR}/clients/python

unset CLIENT_CONFIG
unset SERVER_CONFIG

while getopts ":c:s:" arg; do
  case $arg in
    c) # Define client configuration
      CLIENT_CONFIG="${OPTARG}"
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
NSCONFIG=$(echo "${SERVER_CONFIG}" | jq length)
for (( ii=0; ii<NSCONFIG; ii++ ))
do
    SCONFIG=$(echo "${SERVER_CONFIG}" | jq .[${ii}] )
    python "${PYTHON_DIR}"/test/e2e/setup_e2e_pytest.py "${CLIENT_CONFIG}" "${SCONFIG}"
    (
      # run in subshell to ensure env doesnt survive
      pytest "${PYTHON_DIR}"/test/e2e -p env
    )
done
