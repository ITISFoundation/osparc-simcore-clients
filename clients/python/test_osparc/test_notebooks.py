import papermill as pm
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil


def test_run_notebooks():
    """Run all notebooks in the documentation
    """
    docs_dir:Path = Path(__file__).parent.parent / 'docs'
    assert docs_dir.is_dir()
    for nb in docs_dir.glob("*.ipynb"):
        print(f"Testing {nb.relative_to(docs_dir)}")
        assert nb.is_file(), f'{nb.relative_to(docs_dir)} is not a file'
        with TemporaryDirectory() as tmp_dir:
            tmp_nb = Path(tmp_dir) / nb.name
            shutil.copy(nb, tmp_nb)
            assert tmp_nb.is_file(), 'Did not succeed to copy notebook'
            output:Path = Path(tmp_dir) / (tmp_nb.stem + '_output.ipynb')
            pm.execute_notebook(input_path=tmp_nb, output_path=output)
