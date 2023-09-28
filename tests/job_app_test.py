import jh_trakr.job_app as job_app
import pytest
import sqlite3
import shutil
import os

TEST_DB = "test_database.db"
TEST_DB_NO_SFX = TEST_DB.split('.')[0]

illegal_chars = ["\\", "/", ":", "\"", "*", "?", "<", ">",
                 "|", " ", "\t", "\n", "\v", "\r", "\'"]


@pytest.mark.sanitize_filename
@pytest.mark.parametrize('illegal_char', illegal_chars)
def test_sanitize_filename(illegal_char):

    res = job_app.sanitize_filename(illegal_char)

    assert res == "_"


@pytest.fixture()
def cleanup_test_db():
    yield
    os.remove(TEST_DB)


@pytest.mark.new_app
def test_new_app_creates_db(cleanup_test_db):
    test_args = ["Company",
                 "Position",
                 "Location",
                 "URL"]
    job_app.new_app(database=TEST_DB, test_args=test_args)

    assert os.path.exists(TEST_DB)


@pytest.mark.new_app
def test_new_app_creates_dirs(cleanup_test_db):
    test_args = ["Company",
                 "Position",
                 "Location",
                 "URL"]
    id = job_app.new_app(database=TEST_DB, test_args=test_args)

    assert os.path.exists("working")
    assert os.path.exists(os.path.join("working", f"Position-at-Company-{id}"))


@pytest.mark.new_app
def test_new_app_correct_db_entry(cleanup_test_db):
    test_args = ["Company",
                 "Position",
                 "Location",
                 "URL"]
    id = job_app.new_app(database=TEST_DB, test_args=test_args)

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


@pytest.fixture()
def hide_working_dir():
    if os.path.exists("working"):
        shutil.move("working", "working.bak")
    yield
    if os.path.exists("working.bak"):
        shutil.move("working.bak", "working")


@pytest.mark.applied_to_app
def test_applied_to_app_no_working_dir_fail(capsys, hide_working_dir):
    with pytest.raises(SystemExit) as exit_info:
        job_app.applied_to_app()

    assert "No working directory" in capsys.readouterr().out
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.fixture()
def hide_database():
    if os.path.exists(job_app.STD_DB):
        shutil.move(job_app.STD_DB, job_app.STD_DB.join(".bak"))
    yield
    if os.path.exists(job_app.STD_DB.join(".bak")):
        shutil.move(job_app.STD_DB.join(".bak"), job_app.STD_DB)


@pytest.mark.applied_to_app
def test_applied_to_app_db_exists(capsys, hide_database):
    with pytest.raises(SystemExit) as exit_info:
        job_app.applied_to_app()

    assert "No database file" in capsys.readouterr().out
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


# def test_applied_to_app_creates_dirs():
#     pass
#
#
# def test_applied_to_app_successful_mv():
#     pass
#
#
# """ These tests might also have common setup/teardown """
#
#
# def test_rejected_from_app_applied_dir_exists():
#     pass
#
#
# def test_rejected_from_app_db_exists():
#     pass
#
#
# def test_rejected_from_app_creates_dirs():
#     pass
#
#
# def test_rejected_from_app_successful_mv():
#     pass
#
#
# """ show_apps tests setup/teardown """
#
#
# def test_show_apps_db_exists():
#     pass
