#!/bin/bash

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

doc="Install osparc python client\n"
doc+="Input:\n"
doc+="------\n"
doc+="\tA single json string. This json string is expected to be the output of setup_client_config.bash or as logged in the pyproject.toml"

print_doc() { echo -e "$doc"; }
[ $# -eq 0 ] && print_doc && exit 0

osparc_client_config=$1




if [[ $(echo "$osparc_client_config" | jq 'has("osparc_client_version")') == "true" ]]; then
  osparc_client_version=$(echo "${osparc_client_config}" | jq -r .osparc_client_version)
  v_string=""
  if [[ "${osparc_client_version}" != "latest" ]]; then
    v_string="==${osparc_client_version}"
  fi
  python -m pip install osparc"${v_string}" --force-reinstall
else
  osparc_client_repo=$(echo "${osparc_client_config}" | jq -r .osparc_client_repo)
  osparc_client_runid=$(echo "${osparc_client_config}" | jq -r .osparc_client_runid)
  tmp_dir=$(mktemp -d)
  pushd "${tmp_dir}"
  echo "gh run download ${osparc_client_runid} --repo=${osparc_client_repo}"
  gh run download "${osparc_client_runid}" --repo="${osparc_client_repo}"
  popd
  osparc_wheel=$(ls "${tmp_dir}"/osparc_python_wheels/osparc-*.whl)
  python -m pip install "${osparc_wheel}" --find-links="${tmp_dir}"/osparc_python_wheels --force-reinstall
  rm -rf "${tmp_dir}"
fi
