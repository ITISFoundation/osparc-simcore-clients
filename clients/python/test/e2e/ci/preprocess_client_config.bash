#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

doc="Setup client configuration for e2e testing of the osparc python client\n"
doc+="Input:\n"
doc+="------\n"
doc+="\tA single json string containing either the field client_version or the two fields client_repo and osparc_client_branch with an optional field client_dev_features.\n"
doc+="\tclient_version can either be the version of a client (e.g. \"0.5.0\") or \"latest\"\n"
doc+="\tExample 1: bash setup_client_config.bash '{\"client_repo\": \"ITISFoundation/osparc-simcore-clients\", \"client_branch\": \"master\"}'\n"
doc+="\tExample 2: bash setup_client_config.bash '{\"client_version\": \"0.5.0\"}'\n"
doc+="Output:\n"
doc+="-------\n"
doc+="\tA json string which, when passed to install_osparc_python_client.bash installs the wanted python client"

print_doc() { echo -e "$doc"; }
[ $# -eq 0 ] && print_doc && exit 0

client_workflow=build-and-test-python-client
client_config=$1

# extract keys from input json
if [[ $(echo "$client_config" | jq 'has("client_version")') == "true" ]]; then
  if [[ $(echo "$client_config" | jq 'length') != 1 ]]; then
    echo "${client_config} was invalid"
    exit 1
  fi
else
  if [[ $(echo "$client_config" | jq 'length') != 2 && $(echo "$client_config" | jq 'length') != 3 ]]; then
    echo "${client_config} was invalid"
    exit 1
  fi
  if [[ $(echo "$client_config" | jq 'has("client_branch")') != "true" || $(echo "$client_config" | jq 'has("client_repo")') != "true" ]]; then
    echo "${client_config} was invalid"
    exit 1
  fi
  client_repo=$(echo "$client_config" | jq -r '.client_repo')
  client_branch=$(echo "$client_config" | jq -r '.client_branch')
  client_runid=$(gh run list --repo="${client_repo}" --branch="${client_branch}" --workflow="${client_workflow}" --limit=100 --json=databaseId,status --jq='map(select(.status=="completed")) | .[0].databaseId')
  client_config=$(echo "${client_config}" | jq --arg cwfw "${client_workflow}" '. += {"client_workflow": $cwfw}')
  client_config=$(echo "${client_config}" | jq --arg crid "${client_runid}" '. += {"client_runid": $crid}')
fi

echo "${client_config}"
