# Python 3.11 is the client's declared floor (`python_requires` in clients/python/setup.py),
# so the e2e suite keeps exercising it. Debian bookworm is supported to 2028.
FROM python:3.11-slim-bookworm

# uv, so the e2e setup does not bootstrap itself with pip. Bump it together with
# IMAGE_VERSION in build-n-publish.bash.
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /usr/local/bin/uv

# git and make: the GitLab CI using this image clones the client repository and installs
# through `make install-e2e-test`. curl fetches a deployment's configuration, jq parses it
# and pip's installation report.
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
        jq \
        make \
    && rm -rf /var/lib/apt/lists/*

CMD [ "/bin/bash" ]
