import jh_trakr.job_app as job_app
import pytest
import sqlite3
import shutil
import os


TEST_DB = "test_database.db"
TEST_DB_NO_SFX = TEST_DB.split('.')[0]
TEST_WORK_DIR = "working_test"


@pytest.fixture()
def cleanup_test_db():
    working_existed = os.path.exists(TEST_WORK_DIR)
    yield
    os.remove(TEST_DB)
    if not working_existed:
        shutil.rmtree(TEST_WORK_DIR)


@pytest.mark.new_app
def test_new_app_creates_db(cleanup_test_db):
    test_args = ["Company",
                 "Position",
                 "Location",
                 "URL"]
    job_app.new_app(database=TEST_DB, test_args=test_args,
                    work_dir=TEST_WORK_DIR)

    assert os.path.exists(TEST_DB)


@pytest.mark.new_app
def test_new_app_creates_dirs(cleanup_test_db):
    test_args = ["Company",
                 "Position",
                 "Location",
                 "URL"]
    id = job_app.new_app(database=TEST_DB, test_args=test_args,
                         work_dir=TEST_WORK_DIR)

    assert os.path.exists(TEST_WORK_DIR)
    assert os.path.exists(os.path.join(TEST_WORK_DIR,
                                       f"Position-at-Company-{id}"))


@pytest.mark.new_app
def test_new_app_correct_db_entry(cleanup_test_db):
    test_args = ["Company",
                 "Position",
                 "Location",
                 "URL"]
    id = job_app.new_app(database=TEST_DB, test_args=test_args,
                         work_dir=TEST_WORK_DIR)

    with sqlite3.connect(TEST_DB) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {TEST_DB_NO_SFX} WHERE id = {id};")
        row = cur.fetchone()

    assert "Company" in row
    assert "Position" in row
    assert "Location" in row
    assert "URL" in row
    assert "working" in row
    assert id in row
