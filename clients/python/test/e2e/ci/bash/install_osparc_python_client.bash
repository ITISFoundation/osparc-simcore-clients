#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

doc="Install osparc python client\n"
doc+="Input:\n"
doc+="------\n"
doc+="\tA single json string containing either the field 'dev_features' as well as 'version'\n"
doc+="\t'version' must either be a semantic version, equal to 'latest_release' or equal to 'latest_master'. 'dev_features' must be either 'true' or 'false''\n"
doc+="\tExample: bash install_osparc_python_client.bash '{\"dev_features\": \"true\", \"version\":  \"latest_master\"}'\n"

print_doc() { echo -e "$doc"; }
[ $# -eq 0 ] && print_doc && exit 0

client_config=$1

if [[ $(echo "$client_config" | jq 'has("version")') != "true" ]]; then
  echo "'version' key was missing"
fi
version=$(echo "${client_config}" | jq -r .version)
if [[ $(echo "$client_config" | jq 'has("dev_features")') != "true" ]]; then
  echo "'dev_features' key was missing"
  exit 1
fi

if [[ "${version}" == "latest_master" ]]; then
  python -m pip install osparc --extra-index-url https://test.pypi.org/simple/ --force-reinstall
else
  v_string=""
  if [[ "${version}" != "latest_release" ]]; then
    v_string="==${version}"
  fi
  python -m pip install osparc"${v_string}" --force-reinstall
fi
