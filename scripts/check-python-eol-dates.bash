#!/usr/bin/env bash
# Fails when the end-of-life dates the client ships stop matching endoflife.date.
#
# The table in clients/python/src/osparc/_python_eol.py is a copy of
# https://endoflife.date/api/python.json. A date in it can move, and a new interpreter
# release leaves it a cycle short, after which the client says nothing to users on that
# interpreter. `--check` compares the copy with the API and runs in the lint workflow;
# `--write` rewrites the copy from the API.
set -euo pipefail

for tool in curl jq; do
    command -v "$tool" >/dev/null || {
        echo "check-python-eol-dates: $tool is required, please install it" >&2
        exit 1
    }
done

cd "$(dirname "${BASH_SOURCE[0]}")/.."

MODULE_PATH="clients/python/src/osparc/_python_eol.py"
API_URL="https://endoflife.date/api/python.json"
MODE="${1:---check}"

case "$MODE" in
    --check | --write) ;;
    *)
        echo "usage: ${0##*/} [--check|--write]" >&2
        exit 2
        ;;
esac

# "<minor> <cycle> <eol>" oldest first; cycles without a release date excluded
fetch_api() {
    curl --fail --silent --show-error --retry 3 --retry-all-errors --max-time 60 "$API_URL" |
        jq -r '
            .[]
            | select(.cycle | startswith("3."))
            | select(.eol | type == "string")
            # A cycle is only supported once it has shipped: the API already
            # carries a planned end-of-life date for interpreters that have not
            # been released, and those must not be demanded of the table.
            | select(.releaseDate | type == "string")
            | select(.releaseDate <= (now | strftime("%Y-%m-%d")))
            | "\(.cycle | split(".") | .[1] | tonumber) \(.cycle) \(.eol)"
        ' |
        sort --numeric-sort --key=1,1
}

# "<minor> <cycle> <eol>" as the module writes it
read_table() {
    sed -nE 's/^[[:space:]]*"3\.([0-9]+)": "([0-9]{4}-[0-9]{2}-[0-9]{2})".*/\1 3.\1 \2/p' \
        "$MODULE_PATH"
}

api="$(fetch_api)"
if [ -z "$api" ]; then
    echo "check-python-eol-dates: $API_URL returned nothing usable" >&2
    exit 1
fi

# An interpreter below the floor cannot install the package, so it is out of scope.
floor="$(sed -nE 's/.*"python_requires": ">=3\.([0-9]+)".*/\1/p' clients/python/setup.py | head -1)"
if [ -z "$floor" ]; then
    echo "check-python-eol-dates: cannot read python_requires from clients/python/setup.py" >&2
    exit 1
fi

if [ "$MODE" = "--write" ]; then
    body="$(printf '%s\n' "$api" | awk -v floor="$floor" \
        '$1 >= floor { printf "    \"3.%s\": \"%s\",\n", $1, $3 }')"
    if [ -z "$body" ]; then
        echo "check-python-eol-dates: the API has no cycle at or above 3.$floor" >&2
        exit 1
    fi
    # Replaces the dict body between its opening brace and the line closing it. The
    # anchor is the symbol alone: matching the annotation as well would let a rewrite
    # of that line replace nothing while still reporting a rewrite.
    if ! awk -v body="$body" '
        !replaced && /_PYTHON_EOL_DATES[^=]*= *\{/ { print; in_body = 1; replaced = 1; print body; next }
        in_body && /^\}/ { in_body = 0 }
        !in_body { print }
        END { if (!replaced) exit 1 }
    ' "$MODULE_PATH" >"$MODULE_PATH.new"; then
        rm -f "$MODULE_PATH.new"
        echo "check-python-eol-dates: no _PYTHON_EOL_DATES table found in $MODULE_PATH" >&2
        exit 1
    fi
    mv "$MODULE_PATH.new" "$MODULE_PATH"
    echo "check-python-eol-dates: rewrote the table in $MODULE_PATH"
    exit 0
fi

table="$(read_table)"
if [ -z "$table" ]; then
    echo "check-python-eol-dates: no dates found in $MODULE_PATH" >&2
    exit 1
fi

failures=0

# Every date the client ships must still be what the API says.
while read -r minor cycle eol; do
    [ -n "$cycle" ] || continue
    current="$(printf '%s\n' "$api" | awk -v c="$cycle" '$2 == c "" { print $3 }')"
    if [ -z "$current" ]; then
        echo "check-python-eol-dates: 3.$minor is in $MODULE_PATH but not in $API_URL" >&2
        failures=1
    elif [ "$current" != "$eol" ]; then
        echo "check-python-eol-dates: 3.$minor reaches end of life on $current, $MODULE_PATH says $eol" >&2
        failures=1
    fi
done <<<"$table"

# Every cycle the client can run on must be in the table, or its users get no warning.
while read -r minor cycle eol; do
    [ "$minor" -ge "$floor" ] || continue
    if ! printf '%s\n' "$table" | grep -q "^[0-9]* 3\.$minor "; then
        echo "check-python-eol-dates: 3.$minor (end of life $eol) is supported but missing from $MODULE_PATH" >&2
        failures=1
    fi
done <<<"$api"

if [ "$failures" -ne 0 ]; then
    echo "check-python-eol-dates: run '$0 --write' to update the table" >&2
fi
exit "$failures"
