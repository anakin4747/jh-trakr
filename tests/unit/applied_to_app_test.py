from jh_trakr.job_app import applied_to_app
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


@pytest.fixture
def hide_working_dir():
    """ Hides "working" directory to ensure error is caught """
    """ Improvements
        - Shadows logic in hide_database, could this be joined?
    """
    shutil.move(TEST_WORK_DIR, TEST_WORK_DIR + ".bak")
    yield
    shutil.move(TEST_WORK_DIR + ".bak", TEST_WORK_DIR)


@pytest.mark.applied_to_app
def test_applied_to_app_no_working_dir_fail(capsys,
                                            cleanup_test_db,
                                            setup_test_new_app,
                                            hide_working_dir):
    """ Tests that if there is no "working" directory the program errors out
    with the correct error message """
    with pytest.raises(SystemExit) as exit_info:
        applied_to_app(work_dir=TEST_WORK_DIR)

    assert "No working directory" in capsys.readouterr().err
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.fixture
def hide_database():
    """ Hides database to ensure error is caught """
    """ Improvements
        - Shadows logic in hide_working_dir, could this be joined?
    """
    shutil.move(TEST_DB, TEST_DB + ".bak")
    yield
    shutil.move(TEST_DB + ".bak", TEST_DB)


@pytest.mark.applied_to_app
def test_applied_to_app_no_db_fail(capsys,
                                   cleanup_test_db,
                                   setup_test_new_app,
                                   hide_database):
    """ Tests that if there is no database the program errors out with the
    correct error message """
    """ Improvements
        - Near duplicate functionality to test_rejected_from_app_no_db_fail
    """
    with pytest.raises(SystemExit) as exit_info:
        applied_to_app(database=TEST_DB, work_dir=TEST_WORK_DIR)

    assert "No database file" in capsys.readouterr().err
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.fixture
def hide_working_app():
    """ Moves application out of working directory so program thinks its
    missing """
    app_dir = os.listdir(TEST_WORK_DIR)[0]
    shutil.move(os.path.join(TEST_WORK_DIR, app_dir), app_dir)
    yield
    shutil.move(app_dir, os.path.join(TEST_WORK_DIR, app_dir))


@pytest.mark.applied_to_app
def test_applied_to_app_no_app_in_working_fail(capsys,
                                               cleanup_test_db,
                                               setup_test_new_app,
                                               hide_working_app):
    """ Tests that if there is no application directory in the working folder
    the program errors out with the correct error message """
    with pytest.raises(SystemExit) as exit_info:
        applied_to_app(database=TEST_DB, work_dir=TEST_WORK_DIR)

    assert "No working application" in capsys.readouterr().err
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.mark.applied_to_app
def test_applied_to_app_creates_dirs(cleanup_test_db, setup_test_new_app):
    """ Tests that applied_to_app creates applied directory """

    """ Improvements
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
    """
    assert not os.path.exists(TEST_APPL_DIR)

    test_arg = "Position-at-Company-1"
    applied_to_app(database=TEST_DB, test_args=test_arg,
                   work_dir=TEST_WORK_DIR, applied_dir=TEST_APPL_DIR)

    assert os.path.exists(TEST_APPL_DIR)
    assert len(os.listdir(TEST_APPL_DIR)) == 1


@pytest.mark.applied_to_app
def test_applied_to_app_successful_mv(cleanup_test_db, setup_test_new_app):
    """ Tests that applied_to_app successfully moved application folder from
    working to applied """

    """ Improvements
        - Refactor test_args so that it can be parameterized and ran with data
          from the faker module
    """
    assert len(os.listdir(TEST_WORK_DIR)) == 1

    test_arg = "Position-at-Company-1"  # REFACTOR to be parameterized
    applied_to_app(database=TEST_DB, test_args=test_arg,
                   work_dir=TEST_WORK_DIR, applied_dir=TEST_APPL_DIR)

    assert os.path.exists(TEST_WORK_DIR)
    assert len(os.listdir(TEST_WORK_DIR)) == 0
