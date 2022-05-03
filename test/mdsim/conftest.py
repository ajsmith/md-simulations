from pathlib import Path

import pytest


test_dir = Path(__file__).parent.resolve()

def test_file_path(name):
    return test_dir / name


@pytest.fixture(autouse=True)
def stride_file_paths():
    file_names = [
        'ibu1.dat',
        'ibu2.dat',
        'water5.dat',
        'water6.dat',
    ]
    return [test_file_path(name) for name in file_names]
