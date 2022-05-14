from pathlib import Path

import pytest


test_dir = Path(__file__).parent.resolve()


@pytest.fixture(autouse=True)
def stride_file_paths():
    file_names = [
        'ibu1.dat',
        'ibu2.dat',
        'water5.dat',
        'water6.dat',
    ]
    return [test_dir / name for name in file_names]


@pytest.fixture(autouse=True)
def contact_file_paths():
    file_names = [
        'ibuContacts1.dat',
        'ibuContacts2.dat',
    ]
    return [test_dir / name for name in file_names]
