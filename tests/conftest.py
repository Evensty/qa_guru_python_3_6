import os
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
res_dir = os.path.join(current_dir, 'resources')
archive = os.path.join(res_dir, 'resources.zip')


@pytest.fixture()
def remove_zip_after_tests():
    yield
    if os.path.exists(archive):
        os.remove(archive)
