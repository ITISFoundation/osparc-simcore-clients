#!/bin/bash

# Generate version <semantic version of last tag(=release)>+<number of commits from last tagged commit>
# This is done by inspecting the tags on the git repo https://github.com/ITISFoundation/osparc-simcore-clients

set -o errexit  # abort on nonzero exitstatus
set -o nounset  # abort on unbound variable
set -o pipefail # don't hide errors within pipes

trap "{ echo 'Could not generate a version file. Probably you need to sync your fork.' >&2; }" ERR

release_info=$(git ls-remote --tags --refs --sort=version:refname https://github.com/ITISFoundation/osparc-simcore-clients | tail -1)
released_version=$(echo "${release_info}" | grep -oP '(?<=refs/tags/v)\d+\.\d+\.\d+')
released_commit=$(echo "${release_info}" | grep -oE '^[[:alnum:]]+')
current_commit=$(git rev-parse HEAD)


# Determines how many commits since the last release and adds that as `dev` index.
merge_base=$(git merge-base "${released_commit}" "${current_commit}")
n_commits_to_merge_base=$(git rev-list --count "${merge_base}".."${current_commit}")


# NOTE:
#   - we develop using post-release versioning
#       - i.e. 1.2.3.post0.devN where N is the number of commits with respect to last release 1.2.3)
#       - Another approach would be using a pre-release version but we do not want to decide on that version
#   - the releases are of the type  1.2.3
#   - we never do post releases as 1.2.3.postX but instead use patches i.e. 1.2.4
#   - the releases are defined using git tags (that is the case with n_commits_to_merge_base=0 )
#   - SEE .github/workflows/publish-python-client.yml for more details
#
if [ "$n_commits_to_merge_base" -gt 0 ]; then
    echo "${released_version}.post0.dev${n_commits_to_merge_base}"
elif [ "$n_commits_to_merge_base" -eq 0 ]; then
    echo "${released_version}"
else
    echo "Error: n_commits_to_merge_base is negative. This should not happen." >&2
    exit 1
fi
