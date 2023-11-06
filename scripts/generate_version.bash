#!/bin/bash

# Generate version <semantic version of last tag(=release)>+<number of commits from last tagged commit>
# This is done by inspecting the tags on the git repo https://github.com/ITISFoundation/osparc-simcore-clients

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

trap "{ echo 'Could not generate a version file. Probably you need to sync your fork.' >&2; }" ERR

release_info=$(git ls-remote --tags --refs --sort=version:refname https://github.com/ITISFoundation/osparc-simcore-clients | tail -1)
release_version=$(echo "${release_info}" | grep -oP '(?<=refs/tags/v)\d+\.\d+\.\d+')
release_commit=$(echo "${release_info}" | grep -oE '^[[:alnum:]]+')
current_commit=$(git rev-parse HEAD)

merge_base=$(git merge-base "${release_commit}" "${current_commit}")
n_commits_to_merge_base=$(git rev-list --count "${merge_base}".."${current_commit}")
echo -n "${release_version}.post${n_commits_to_merge_base}"
