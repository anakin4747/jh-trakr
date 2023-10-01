from jh_trakr.job_app import (new_app, applied_to_app,
                              rejected_from_app, sanitize_filename)
import pytest
import shutil
import os


""" Improvements
    - Add test to ensure fzf errors out properly
    - Check for correct db entry (see test_new_app_correct_db_entry)
"""


TEST_DB = "test_database.db"
TEST_WORK_DIR = "working_test"
TEST_APPL_DIR = "applied_test"
TEST_REJ_DIR = os.path.join(TEST_APPL_DIR, "rejected_test")


@pytest.fixture
def setup_test_applied_app():
    """ Run new_app and applied_to_app so that a db and application exists """

    """ Improvements
        - Shares teardown logic of clean_up_db fixture in new_app_test
        - Shares setup/teardown logic of setup_test_new_app fixture in
          new_app_test
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
        - Figure out how to remove the hard coded id of 1 in applied_to_app
    """
    test_args = ["Company", "Position", "Location", "URL"]
    new_app(database=TEST_DB, test_args=test_args, work_dir=TEST_WORK_DIR)

    title = sanitize_filename(f"{test_args[1]}-at-{test_args[0]}")
    applied_to_app(database=TEST_DB, test_args=f"{title}-1",
                   work_dir=TEST_WORK_DIR, applied_dir=TEST_APPL_DIR)
    yield
    if os.path.exists(TEST_REJ_DIR):
        shutil.rmtree(TEST_REJ_DIR)
    if os.path.exists(TEST_APPL_DIR):
        shutil.rmtree(TEST_APPL_DIR)
    shutil.rmtree(TEST_WORK_DIR)
    os.remove(TEST_DB)


@pytest.fixture
def hide_applied_dir():
    """ Hides "applied" directory to ensure error is caught """
    """ Improvements
        - Shadows logic in hide_database and hide_working_dir,
          could this be joined?
    """
    shutil.move(TEST_APPL_DIR, TEST_APPL_DIR + ".bak")
    yield
    shutil.move(TEST_APPL_DIR + ".bak", TEST_APPL_DIR)


@pytest.mark.rejected_from_app
def test_rejected_from_app_no_applied_dir_fail(capsys,
                                               setup_test_applied_app,
                                               hide_applied_dir):
    """ Tests that if there is no application directory the program errors out 
    with the correct error message """
    with pytest.raises(SystemExit) as exit_info:
        rejected_from_app(database=TEST_DB, applied_dir=TEST_APPL_DIR)

    assert "No applied directory" in capsys.readouterr().err
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.fixture
def hide_database():
    """ duplicate from applied_to_app_test """
    shutil.move(TEST_DB, TEST_DB + ".bak")
    yield
    shutil.move(TEST_DB + ".bak", TEST_DB)


@pytest.mark.rejected_from_app
def test_rejected_from_app_no_db_fail(capsys,
                                      setup_test_applied_app,
                                      hide_database):
    """ Tests that if there is no database the program errors out with the
    correct error message """
    """ Improvements
        - Near duplicate functionality to test_applied_to_app_no_db_fail
    """
    with pytest.raises(SystemExit) as exit_info:
        rejected_from_app(database=TEST_DB, applied_dir=TEST_APPL_DIR)

    assert "No database file" in capsys.readouterr().err
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.fixture
def hide_applied_app():
    """ Duplicate """
    app_dir = os.listdir(TEST_APPL_DIR)[0]
    shutil.move(os.path.join(TEST_APPL_DIR, app_dir), app_dir)
    yield
    shutil.move(app_dir, os.path.join(TEST_APPL_DIR, app_dir))


@pytest.mark.rejected_from_app
def test_rejectd_from_app_no_app_in_applied_fail(capsys,
                                                 setup_test_applied_app,
                                                 hide_applied_app):
    """ Tests that if there is no application directory in the applied folder
    the program errors out with the correct error message """
    with pytest.raises(SystemExit) as exit_info:
        rejected_from_app(database=TEST_DB, applied_dir=TEST_APPL_DIR)

    assert "No applied application" in capsys.readouterr().err
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.mark.rejected_from_app
def test_rejected_from_app_creates_dirs(setup_test_applied_app):
    """ Tests that rejected_from_app creates rejected directory """

    """ Improvements
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
    """
    assert not os.path.exists(TEST_REJ_DIR)

    test_arg = "Position-at-Company-1"
    rejected_from_app(database=TEST_DB, test_args=test_arg,
                      applied_dir=TEST_APPL_DIR, rej_dir=TEST_REJ_DIR)

    assert os.path.exists(TEST_REJ_DIR)
    assert len(os.listdir(TEST_REJ_DIR)) == 1


@pytest.mark.rejected_from_app
def test_rejected_from_app_successful_mv(setup_test_applied_app):
    """ Tests that rejected_from_app successfully moved application folder from
    applied to rejected """

    """ Improvements
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
    """
    assert len(os.listdir(TEST_APPL_DIR)) == 1

    test_arg = "Position-at-Company-1"
    rejected_from_app(database=TEST_DB, test_args=test_arg,
                      applied_dir=TEST_APPL_DIR, rej_dir=TEST_REJ_DIR)

    assert os.path.exists(TEST_APPL_DIR)
    assert len(os.listdir(TEST_REJ_DIR)) == 1
