import re

import typer

# Regex pattern for determining whether a string is a
# valid semantic version (found here: https://semver.org/)
_SemVerPattern: str = (
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))"
    r"?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def main(string: str, raise_failure: bool = True):
    result: str = "0"
    if re.match(_SemVerPattern, string):
        result = "1"
    print(result)
    if raise_failure:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
