from jh_trakr.job_app import rejected_from_app
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
