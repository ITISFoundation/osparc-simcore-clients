import typer
from _utils import _PYPROJECT_TOML
import toml
from _utils import ClientConfig, ServerConfig, E2eExitCodes, _COMPATIBILITY_JSON
from pydantic import ValidationError
import pandas as pd
import pytest

def main() -> None:
  """ Checks if the client x server configuration in the pyproject.toml is compatible
  """
  try:
    pytest_envs = toml.load(_PYPROJECT_TOML)["tool"]["pytest"]["ini_options"]["env"]
    client_cfg: ClientConfig = ClientConfig(**toml.load(_PYPROJECT_TOML)['client'])
    server_cfg: ServerConfig = ServerConfig(**dict([tuple(s.strip(' ') for s in elm.split('=')) for elm in pytest_envs]))
  except (Exception, ValidationError) as e:
    print(e)
    raise typer.Exit(code=E2eExitCodes.INVALID_JSON_DATA)

  compatibility_df: pd.DataFrame = pd.read_json(_COMPATIBILITY_JSON)

  if not client_cfg.client_ref in compatibility_df.columns:
    print(f"The client ref '{client_cfg.client_ref}' could not be found in {_COMPATIBILITY_JSON}")
    raise typer.Exit(code=E2eExitCodes.INVALID_CLIENT_VS_SERVER)
  if not server_cfg.url.netloc in compatibility_df.index:
    print(f"The server netloc '{server_cfg.url.netloc}' could not be found in {_COMPATIBILITY_JSON}")

  if not compatibility_df[client_cfg.client_ref][server_cfg.url.netloc]:
    raise typer.Exit(code=E2eExitCodes.INVALID_CLIENT_VS_SERVER)
  else:
    raise typer.Exit(code=pytest.ExitCode.OK)







if __name__ == '__main__':
  typer.run(main)
