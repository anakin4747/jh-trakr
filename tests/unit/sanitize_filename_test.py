from jh_trakr.job_app import sanitize_filename
import pytest

illegal_chars = ["\\", "/", ":", "\"", "*", "?", "<", ">",
                 "|", " ", "\t", "\n", "\v", "\r", "\'"]


@pytest.mark.sanitize_filename
@pytest.mark.parametrize('illegal_char', illegal_chars)
def test_sanitize_filename(illegal_char):

    res = sanitize_filename(illegal_char)

    assert res == "_"
