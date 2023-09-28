import jh_trakr.job_app as job_app
import pytest

illegal_chars = ["\\", "/", ":", "\"", "*", "?", "<", ">",
                 "|", " ", "\t", "\n", "\v", "\r", "\'"]


@pytest.mark.sanitize_filename
@pytest.mark.parametrize('illegal_char', illegal_chars)
def test_sanitize_filename(illegal_char):

    res = job_app.sanitize_filename(illegal_char)

    assert res == "_"
