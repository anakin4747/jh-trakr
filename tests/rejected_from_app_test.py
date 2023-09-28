import jh_trakr.job_app as job_app
import pytest
import shutil
import os


TEST_DB = "test_database.db"
TEST_WORK_DIR = "working_test"
TEST_APPL_DIR = "applied_test"
TEST_REJ_DIR = os.path.join(TEST_APPL_DIR, "rejected_test")


@pytest.fixture
def setup_test_applied_app():
    test_args = ["Company", "Position", "Location", "URL"]
    job_app.new_app(database=TEST_DB,
                    test_args=test_args,
                    work_dir=TEST_WORK_DIR)
    job_app.applied_to_app(database=TEST_DB,
                           test_args="Position-at-Company-1",
                           work_dir=TEST_WORK_DIR,
                           applied_dir=TEST_APPL_DIR)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    if os.path.exists(TEST_WORK_DIR):
        shutil.rmtree(TEST_WORK_DIR)
    if os.path.exists(TEST_REJ_DIR):
        shutil.rmtree(TEST_REJ_DIR)
    if os.path.exists(TEST_APPL_DIR):
        shutil.rmtree(TEST_APPL_DIR)


@pytest.fixture
def hide_applied_dir():
    if os.path.exists(TEST_APPL_DIR):
        shutil.move(TEST_APPL_DIR, TEST_APPL_DIR + ".bak")
    yield
    if os.path.exists(TEST_APPL_DIR + ".bak"):
        shutil.move(TEST_APPL_DIR + ".bak", TEST_APPL_DIR)


@pytest.mark.rejected_from_app
def test_rejected_from_app_no_applied_dir_fail(capsys,
                                              setup_test_applied_app,
                                              hide_applied_dir):
    with pytest.raises(SystemExit) as exit_info:
        job_app.rejected_from_app(database=TEST_DB,
                                  applied_dir=TEST_APPL_DIR)

    assert "No applied directory" in capsys.readouterr().out
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.fixture
def hide_database():
    if os.path.exists(TEST_DB):
        shutil.move(TEST_DB, TEST_DB + ".bak")
    yield
    if os.path.exists(TEST_DB + ".bak"):
        shutil.move(TEST_DB + ".bak", TEST_DB)


@pytest.mark.rejected_from_app
def test_rejected_from_app_no_db_fail(capsys,
                                      setup_test_applied_app,
                                      hide_database):
    with pytest.raises(SystemExit) as exit_info:
        job_app.rejected_from_app(database=TEST_DB,
                                  applied_dir=TEST_APPL_DIR)

    assert "No database file" in capsys.readouterr().out
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.fixture
def hide_applied_app():
    app_dir = os.listdir(TEST_APPL_DIR)[0]
    shutil.move(os.path.join(TEST_APPL_DIR, app_dir), app_dir)
    yield
    shutil.move(app_dir, os.path.join(TEST_APPL_DIR, app_dir))


@pytest.mark.rejected_from_app
def test_rejectd_from_app_no_app_in_applied_fail(capsys,
                                                 setup_test_applied_app,
                                                 hide_applied_app):
    with pytest.raises(SystemExit) as exit_info:
        job_app.rejected_from_app(database=TEST_DB,
                                  applied_dir=TEST_APPL_DIR)

    assert "No applied application" in capsys.readouterr().out
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.mark.rejected_from_app
def test_rejected_from_app_creates_dirs(setup_test_applied_app):
    test_arg = "Position-at-Company-1"
    job_app.rejected_from_app(database=TEST_DB,
                              test_args=test_arg,
                              applied_dir=TEST_APPL_DIR,
                              rej_dir=TEST_REJ_DIR)

    assert os.path.exists(TEST_REJ_DIR)
    assert len(os.listdir(TEST_REJ_DIR)) == 1


@pytest.mark.rejected_from_app
def test_rejected_from_app_successful_mv(setup_test_applied_app):
    assert len(os.listdir(TEST_APPL_DIR)) == 1

    test_arg = "Position-at-Company-1"
    job_app.rejected_from_app(database=TEST_DB,
                              test_args=test_arg,
                              applied_dir=TEST_APPL_DIR,
                              rej_dir=TEST_REJ_DIR)

    assert os.path.exists(TEST_APPL_DIR)
    assert len(os.listdir(TEST_REJ_DIR)) == 1


