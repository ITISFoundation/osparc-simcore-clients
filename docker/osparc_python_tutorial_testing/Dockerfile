# Python 3.11 is the client's declared floor (`python_requires` in clients/python/setup.py),
# so the e2e suite keeps exercising it. Debian trixie (13) is current stable: supported to
# 2030 and LTS to 2035, against bookworm's 2028.
#
# The libc is deliberately glibc. An alpine (musl) base is 225 MB smaller, but it makes the
# suite install musllinux wheels that no osparc deployment ever loads.
FROM python:3.11-slim-trixie

# uv, so the e2e setup does not bootstrap itself with pip. Bump it together with
# IMAGE_VERSION in build-n-publish.bash.
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /usr/local/bin/uv

# git and make: the GitLab CI using this image clones the client repository and installs
# through `make install-e2e-test`. curl fetches a deployment's configuration, jq parses it
# and pip's installation report.
#
# This layer is 144 MB and almost all of it is `git`: perl (32 MB), 25 MB of
# /usr/lib/git-core, git-man, and Debian has no slim git variant. curl, jq and make together
# are under 4 MB, so keep this list to what a CI job actually runs.
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
        jq \
        make \
    && rm -rf /var/lib/apt/lists/*

CMD [ "/bin/bash" ]
