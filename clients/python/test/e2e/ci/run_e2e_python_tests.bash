#!/bin/bash

set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

CI_DIR=$(realpath "$(dirname "$0")")

doc="Run e2e osparc python client tests\n"
doc+="Input:\n"
doc+="------\n"
doc+="\tTwo json strings: A client json configuration and a server json configuration. Example: \"bash run_e2e_python_tests.bash -c <client json> -s <server json>\".\n"
doc+="\tThe client array must adhere to the requirements of setup_client_config.bash (run \"bash setup_client_config.bash\").\n"
doc+="\tThe server json string must be an array of json objects. Each json object must contain the following fields:\n"
doc+="\t\t - OSPARC_API_HOST\n"
doc+="\t\t - OSPARC_API_KEY\n"
doc+="\t\t - OSPARC_API_SECRET\n"
doc+="\tExample: [{\"OSPARC_API_HOST\":\"https://api.osparc-master.speag.com\", \"OSPARC_API_KEY\":\"mykey\", \"OSPARC_API_SECRET\":\"mysecret\"}] \n"
doc+="Output:\n"
doc+="-------\n"
doc+="\tTest results are stored in clients/python/artifacts/e2e/<client branch or version>.json and the \"pyproject.toml\" file from which one can completely\n"
doc+="\treproduce the testrun is stored in clients/python/artifacts/e2e/<branch+server_url>/pyproject.toml\n"

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

if [[ "$(echo "${OSPARC_SERVER_CONFIGS}" | jq 'type == "array"')" != "true" ]]; then
  echo -e "The server configuration (-s) must a an array of json objects. Received: ${OSPARC_SERVER_CONFIGS}"; exit 1
fi

NSCONFIG=$(echo "${OSPARC_SERVER_CONFIGS}" | jq length)
for (( ii=0; ii<NSCONFIG; ii++ ))
do
    SCONFIG=$(echo "${OSPARC_SERVER_CONFIGS}" | jq .[${ii}] )
    if ! python "${CI_DIR}"/generate_pytest_ini.py "${OSPARC_CLIENT_CONFIG}" "${SCONFIG}"; then
      exit 1
    fi
    python "${CI_DIR}"/compatible_client_server.py
    EC=$?
    if [[ "${EC}" -ne 0 ]]; then
      if ! python "${CI_DIR}"/postprocess_e2e.py "${EC}"; then
        exit 1
      fi
      continue
    fi
    (
      # run in subshell to ensure env doesnt survive
      python -m pytest -c pytest.ini > /dev/null
      if ! python "${CI_DIR}"/postprocess_e2e.py $?; then
        exit 1
      fi
    )
done
