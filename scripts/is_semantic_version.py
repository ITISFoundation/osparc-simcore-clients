import typer
from semver.version import Version as V


def main(version_string: str, raise_result: bool = True):
    """
    Check if a string v is a \"pure\" semantic version. I.e. v=a.b.c
    for positive integers a, b and c. We don't allow prerelease info
    or dev info here.
    """
    result: bool = V.is_valid(version_string)
    if result:
        v: V = V.parse(version_string)
        result = v == V(v.major, v.minor, v.patch)
    if raise_result:
        raise typer.Exit(code=0 if result else 1)
    print(result)


if __name__ == "__main__":
    typer.run(main)
