from jh_trakr.job_app import new_app, applied_to_app, sanitize_filename
import pytest
import shutil
import os

TEST_DB = "test_database.db"
TEST_WORK_DIR = "working_test"
TEST_APPL_DIR = "applied_test"
TEST_REJ_DIR = os.path.join(TEST_APPL_DIR, "rejected_test")


@pytest.fixture
def cleanup_test_db():
    """ Removes db file created from new_app calls """
    yield

    shutil.rmtree(TEST_WORK_DIR)
    os.remove(TEST_DB)


@pytest.fixture
def setup_test_new_app():
    """ Run new_app so that a db and application exists """

    """ Improvements
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
    """
    test_args = ["Company", "Position", "Location", "URL"]
    new_app(database=TEST_DB, test_args=test_args, work_dir=TEST_WORK_DIR)

    yield

    if os.path.exists(TEST_APPL_DIR):
        shutil.rmtree(TEST_APPL_DIR)


@pytest.fixture
def setup_test_applied_app():
    """ Run new_app and applied_to_app so that a db and application exists """

    """ Improvements
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
        - Figure out how to remove the hard coded id of 1 in applied_to_app
    """
    test_args = ["Company", "Position", "Location", "URL"]

    title = sanitize_filename(f"{test_args[1]}-at-{test_args[0]}")
    applied_to_app(database=TEST_DB, test_args=f"{title}-1",
                   work_dir=TEST_WORK_DIR, applied_dir=TEST_APPL_DIR)
    yield

    if os.path.exists(TEST_REJ_DIR):
        shutil.rmtree(TEST_REJ_DIR)
