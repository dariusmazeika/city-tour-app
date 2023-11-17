import shutil

import pytest

from conf.settings_test import TEST_DIR


@pytest.fixture()
def cleanup_media_folder():
    yield
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
