
import typer
from _utils import _PYPROJECT_TOML
import toml


def main() -> None:
  """ Checks if the client x server configuration in the pyproject.toml is compatible
  """
  client_cfg = toml.load(_PYPROJECT_TOML)['client']
  print(client_cfg)



if __name__ == '__main__':
  typer.run(main)
