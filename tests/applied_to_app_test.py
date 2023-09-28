import jh_trakr.job_app as job_app
import pytest
import shutil
import os


TEST_DB = "test_database.db"
TEST_DB_NO_SFX = TEST_DB.split('.')[0]
TEST_WORK_DIR = "working_test"


@pytest.fixture
def setup_test_db_and_dirs():
    test_args = ["Company", "Position", "Location", "URL"]
    job_app.new_app(database=TEST_DB,
                    test_args=test_args,
                    work_dir=TEST_WORK_DIR)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    if os.path.exists(TEST_WORK_DIR):
        shutil.rmtree(TEST_WORK_DIR)


@pytest.fixture
def hide_working_dir():
    if os.path.exists(TEST_WORK_DIR):
        shutil.move(TEST_WORK_DIR, TEST_WORK_DIR + ".bak")
    yield
    if os.path.exists(TEST_WORK_DIR + ".bak"):
        shutil.move(TEST_WORK_DIR + ".bak", TEST_WORK_DIR)


@pytest.mark.applied_to_app
def test_applied_to_app_no_working_dir_fail(capsys,
                                            setup_test_db_and_dirs,
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
                                   setup_test_db_and_dirs,
                                   hide_database):
    with pytest.raises(SystemExit) as exit_info:
        job_app.applied_to_app(database=TEST_DB,
                               work_dir=TEST_WORK_DIR)

    assert "No database file" in capsys.readouterr().out
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1


# @pytest.fixture()
# def hide_working_apps():
#     if os.path.exists("working"):
#         for dir in os.listdir("working"):
#             shutil.move("working/" + dir, "working.bak/" + dir)
#     yield
#     if os.path.exists("working.bak"):
#         for dir in os.listdir("working.bak"):
#             shutil.move("working.bak/" + dir, "working/" + dir)
#         shutil.rmtree("working.bak")
#
#
# @pytest.mark.applied_to_app
# def test_applied_to_app_no_app_in_working_fail(capsys, hide_working_apps,
#                                                mktmpdir_working):
#     with pytest.raises(SystemExit) as exit_info:
#         job_app.applied_to_app(database=TEST_DB)
#
#     assert "No working application" in capsys.readouterr().out
#     assert exit_info.type == SystemExit
#     assert exit_info.value.code == 1
#
#
# @pytest.fixture()
# def working_job_app():
#     test_args = ["Company",
#                  "Position",
#                  "Location",
#                  "URL"]
#     working_existed = os.path.exists("working")
#
#     id = job_app.new_app(database=TEST_DB, test_args=test_args)
#
#     applied_existed = False
#
#     if os.path.exists("applied"):
#         applied_existed = True
#         for dir in os.listdir("applied"):
#             shutil.move("applied/" + dir, "applied.bak/" + dir)
#     yield
#     os.remove(TEST_DB)
#     if os.path.exists("applied.bak"):
#         for dir in os.listdir("applied.bak"):
#             shutil.move("applied.bak/" + dir, "applied/" + dir)
#     shutil.rmtree(f"applied/Position-at-Company-{id}")
#
#     if not applied_existed:
#         shutil.rmtree("applied")
#
#     if not working_existed:
#         shutil.rmtree("working")
#
#
# @pytest.mark.applied_to_app
# def test_applied_to_app_creates_dirs(working_job_app):
#     test_arg = "Position-at-Company-1"
#     job_app.applied_to_app(database=TEST_DB, test_args=test_arg)
#
#     assert os.path.exists("applied")
#     assert len(os.listdir("applied")) == 1
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
