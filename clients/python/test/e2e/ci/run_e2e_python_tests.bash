#!/bin/bash

set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

CI_DIR=$(realpath "$(dirname "$0")")
E2E_DIR=$(realpath "${CI_DIR}/..")
PYTHON_DIR=$(realpath "${E2E_DIR}/../..")

doc="Run e2e Setup client configuration for e2e testing of the osparc python client\n"
doc+="Input:\n"
doc+="------\n"
doc+="\tA single json string containing the three fields OSPARC_CLIENT_VERSION, OSPARC_CLIENT_REPO and OSPARC_CLIENT_BRANCH and meeting exactly one of the following two conditions:\n"
doc+="\t\t- the field OSPARC_CLIENT_VERSION is empty\n"
doc+="\t\t- the two fields OSPARC_CLIENT_REPO and OSPARC_CLIENT_BRANCH are empty\n"
doc+="\tOSPARC_CLIENT_VERSION can either be the version of a client (e.g. \"0.5.0\") or \"latest\"\n"
doc+="\tExample 1: bash setup_client_config.bash '{\"OSPARC_CLIENT_REPO\": \"ITISFoundation/osparc-simcore-clients\", \"OSPARC_CLIENT_BRANCH\": \"master\", \"OSPARC_CLIENT_VERSION\": \"\"}'\n"
doc+="\tExample 2: bash setup_client_config.bash '{\"OSPARC_CLIENT_REPO\": \"\", \"OSPARC_CLIENT_BRANCH\": \"\", \"OSPARC_CLIENT_VERSION\": \"0.5.0\"}'\n"
doc+="Output:\n"
doc+="-------\n"
doc+="\tA json string which, when passed to install_osparc_python_client.bash installs the wanted python client"

print_doc() { echo -e "$doc"; }
[ $# -eq 0 ] && print_doc && exit 0

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
      print_doc
      exit 1
      ;;
  esac
done

rm -rf "${PYTHON_DIR}"/artifacts || true
if [[ "$(echo "${OSPARC_SERVER_CONFIGS}" | jq 'type == "array"')" != "true" ]]; then
  echo -e "The server configuration (-s) must a an array of json objects. Received: ${OSPARC_SERVER_CONFIGS}"; exit 1
fi

if ! OSPARC_CLIENT_CONFIG=$(bash "${CI_DIR}"/setup_client_config.bash "${OSPARC_CLIENT_CONFIG}"); then
  echo "Could not determine client configuration"; exit 1
fi
if ! bash "${CI_DIR}"/install_osparc_python_client.bash "${OSPARC_CLIENT_CONFIG}"; then
  echo "Could not instal client"; exit 1
fi

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
