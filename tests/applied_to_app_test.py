import jh_trakr.job_app as job_app
import pytest
import shutil
import os


TEST_DB = "test_database.db"
TEST_WORK_DIR = "working_test"
TEST_APPL_DIR = "applied_test"


@pytest.fixture
def setup_test_new_app():
    test_args = ["Company", "Position", "Location", "URL"]
    job_app.new_app(database=TEST_DB,
                    test_args=test_args,
                    work_dir=TEST_WORK_DIR)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    if os.path.exists(TEST_WORK_DIR):
        shutil.rmtree(TEST_WORK_DIR)
    if os.path.exists(TEST_APPL_DIR):
        shutil.rmtree(TEST_APPL_DIR)


@pytest.fixture
def hide_working_dir():
    if os.path.exists(TEST_WORK_DIR):
        shutil.move(TEST_WORK_DIR, TEST_WORK_DIR + ".bak")
    yield
    if os.path.exists(TEST_WORK_DIR + ".bak"):
        shutil.move(TEST_WORK_DIR + ".bak", TEST_WORK_DIR)


@pytest.mark.applied_to_app
def test_applied_to_app_no_working_dir_fail(capsys,
                                            setup_test_new_app,
                                            hide_working_dir):
    with pytest.raises(SystemExit) as exit_info:
        job_app.applied_to_app(work_dir=TEST_WORK_DIR)

    assert "No working directory" in capsys.readouterr().out
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.fixture
def hide_database():
    if os.path.exists(TEST_DB):
        shutil.move(TEST_DB, TEST_DB + ".bak")
    yield
    if os.path.exists(TEST_DB + ".bak"):
        shutil.move(TEST_DB + ".bak", TEST_DB)


@pytest.mark.applied_to_app
def test_applied_to_app_no_db_fail(capsys,
                                   setup_test_new_app,
                                   hide_database):
    with pytest.raises(SystemExit) as exit_info:
        job_app.applied_to_app(database=TEST_DB,
                               work_dir=TEST_WORK_DIR)

    assert "No database file" in capsys.readouterr().out
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.fixture
def hide_working_app():
    app_dir = os.listdir(TEST_WORK_DIR)[0]
    shutil.move(os.path.join(TEST_WORK_DIR, app_dir), app_dir)
    yield
    shutil.move(app_dir, os.path.join(TEST_WORK_DIR, app_dir))


@pytest.mark.applied_to_app
def test_applied_to_app_no_app_in_working_fail(capsys,
                                               setup_test_new_app,
                                               hide_working_app):
    with pytest.raises(SystemExit) as exit_info:
        job_app.applied_to_app(database=TEST_DB,
                               work_dir=TEST_WORK_DIR)

    assert "No working application" in capsys.readouterr().out
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


@pytest.mark.applied_to_app
def test_applied_to_app_creates_dirs(setup_test_new_app):
    test_arg = "Position-at-Company-1"
    job_app.applied_to_app(database=TEST_DB,
                           test_args=test_arg,
                           work_dir=TEST_WORK_DIR,
                           applied_dir=TEST_APPL_DIR)

    assert os.path.exists(TEST_APPL_DIR)
    assert len(os.listdir(TEST_APPL_DIR)) == 1


@pytest.mark.applied_to_app
def test_applied_to_app_successful_mv(setup_test_new_app):
    assert len(os.listdir(TEST_WORK_DIR)) == 1

    test_arg = "Position-at-Company-1"
    job_app.applied_to_app(database=TEST_DB,
                           test_args=test_arg,
                           work_dir=TEST_WORK_DIR,
                           applied_dir=TEST_APPL_DIR)

    assert os.path.exists(TEST_WORK_DIR)
    assert len(os.listdir(TEST_WORK_DIR)) == 0
