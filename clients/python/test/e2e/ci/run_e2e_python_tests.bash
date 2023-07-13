#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

CI_DIR=$(realpath "$(dirname "$0")")
E2E_DIR=$(realpath "${CI_DIR}/..")

unset OSPARC_CLIENT_CONFIG
unset OSPARC_SERVER_CONFIG

while getopts ":c:s:" arg; do
  case $arg in
    c) # Define client configuration
      OSPARC_CLIENT_CONFIG="${OPTARG}"
      ;;
    s) # Define server configuration
      OSPARC_SERVER_CONFIGS="${OPTARG}"
      ;;
    *)
      echo "Received unknown flag"
      exit 1
      ;;
  esac
done

OSPARC_CLIENT_CONFIG=$(bash "${CI_DIR}"/setup_client_config.bash "${OSPARC_CLIENT_CONFIG}")
bash "${CI_DIR}"/install_osparc_python_client.bash "${OSPARC_CLIENT_CONFIG}"

NSCONFIG=$(echo "${OSPARC_SERVER_CONFIGS}" | jq length)
for (( ii=0; ii<NSCONFIG; ii++ ))
do
    SCONFIG=$(echo "${OSPARC_SERVER_CONFIGS}" | jq .[${ii}] )
    python "${CI_DIR}"/setup_e2e_pytest.py "${OSPARC_CLIENT_CONFIG}" "${SCONFIG}"
    (
      # run in subshell to ensure env doesnt survive
      pytest "${E2E_DIR}" -p env
      python "${CI_DIR}"/postprocess_e2e.py $?
    )
done
