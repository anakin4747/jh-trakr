import subprocess
import pytest

""" These tests test command line arguments """

PROG = "python3 jh_trakr/main.py"


def run(program, args):
    return subprocess.run(f"{program} {args}", shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          text=True)


@pytest.mark.main
def test_no_args():
    res = run(PROG, "")
    assert "usage" in res.stderr
    assert res.returncode == 1


@pytest.mark.main
def test_invalid_2nd_arg():
    res = run(PROG, "invalid_arg")
    assert "usage" in res.stderr
    assert res.returncode == 1


@pytest.mark.main
def test_invalid_3rd_arg():
    res = run(PROG, "show invalid_arg")
    assert "show usage" in res.stderr
    assert res.returncode == 1
