from jh_trakr.job_app import new_app, sanitize_filename
import pytest
import sqlite3
import shutil
import os


TEST_DB = "test_database.db"
TEST_DB_NO_SFX = TEST_DB.split('.')[0]
TEST_WORK_DIR = "working_test"


@pytest.fixture
def cleanup_test_db():
    """ Removes db file created from new_app calls """
    """ Improvements
        - Could probably be shared with other fixtures and stacked so that this
          logic isn't repeated
    """
    yield
    shutil.rmtree(TEST_WORK_DIR)
    os.remove(TEST_DB)


@pytest.mark.new_app
def test_new_app_creates_db(cleanup_test_db):
    """ Tests that new_app creates a new database """

    """ Improvemnts
        - test could be improved by checking the .schema of the db matches the
          expected table
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
    """
    test_args = ["Company", "Position", "Location", "URL"]

    new_app(database=TEST_DB, test_args=test_args, work_dir=TEST_WORK_DIR)

    assert os.path.exists(TEST_DB)


@pytest.mark.new_app
def test_new_app_creates_dirs(cleanup_test_db):
    """ Tests that new_app creates working directory and application
    subdirectory """

    """ Improvements
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
    """
    test_args = ["Company", "Position", "Location", "URL"]
    title = sanitize_filename(f"{test_args[1]}-at-{test_args[0]}")
    id = new_app(database=TEST_DB, test_args=test_args, work_dir=TEST_WORK_DIR)

    assert os.path.exists(TEST_WORK_DIR)
    assert os.path.exists(os.path.join(TEST_WORK_DIR, f"{title}-{id}"))


@pytest.mark.new_app
def test_new_app_correct_db_entry(cleanup_test_db):
    """ Tests that new_app creates a correct entry in the database """

    """ Improvemnts
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
    """
    test_args = ["Company", "Position", "Location", "URL"]
    id = new_app(database=TEST_DB, test_args=test_args, work_dir=TEST_WORK_DIR)

    with sqlite3.connect(TEST_DB) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {TEST_DB_NO_SFX} WHERE id = {id};")
        row = cur.fetchone()

    for arg in test_args:
        assert arg in row
    assert "working" in row
    assert id in row
