import papermill as pm
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import pytest
from typing import List, Dict, Any
import sys

docs_dir:Path = Path(__file__).parent.parent / 'docs'
all_notebooks:List[Path] = list(docs_dir.glob("*.ipynb"))


def test_notebook_config():
    """ Checks the jupyter environment is configured correctly
    """
    config_test_nb:Path = Path(__file__).parent / 'data' / 'config_test.ipynb'
    assert config_test_nb.is_file()
    test_run_notebooks(config_test_nb,{'expected_python_bin':sys.executable})
    assert len(all_notebooks) > 0, f'Did now find any notebooks in {docs_dir}'

@pytest.mark.parametrize('notebook,params',list(zip(all_notebooks,[{}]*len(all_notebooks))))
def test_run_notebooks(notebook:Path, params:Dict[str,Any]):
    """Run all notebooks in the documentation
    """
    print(f"Running {notebook.name} with parameters {params}")
    assert notebook.is_file(), f'{notebook.name} is not a file (full path: {notebook.resolve()})'
    with TemporaryDirectory() as tmp_dir:
        tmp_nb = Path(tmp_dir) / notebook.name
        shutil.copy(notebook, tmp_nb)
        assert tmp_nb.is_file(), 'Did not succeed in copying notebook'
        output:Path = Path(tmp_dir) / (tmp_nb.stem + '_output.ipynb')
        pm.execute_notebook(input_path=tmp_nb, output_path=output, kernel_name="python3",parameters=params)
