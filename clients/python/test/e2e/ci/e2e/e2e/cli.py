from typer import Typer

from . import postprocess, preprocess

cli = Typer()
cli.add_typer(preprocess.cli, name="preprocess")
cli.add_typer(postprocess.cli, name="postprocess")
