from jh_trakr.job_app import show_apps
import pytest


TEST_DB = "test_database.db"


@pytest.mark.show_apps
def test_show_apps_no_db_fail(capsys):
    with pytest.raises(SystemExit) as exit_info:
        show_apps(database=TEST_DB)

    assert "No database file" in capsys.readouterr().err
    assert exit_info.type == SystemExit
    assert exit_info.value.code == 1
