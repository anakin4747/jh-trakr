import subprocess

""" These tests test command line arguments """

PROG = "python3 jh_trakr/main.py"


def test_no_args():
    res = subprocess.run(f"{PROG}",
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         text=True)
    assert "usage" in res.stderr
    assert res.returncode == 1


def test_invalid_2nd_arg():
    res = subprocess.run(f"{PROG} invalid_arg",
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         text=True)
    assert "usage" in res.stderr
    assert res.returncode == 1


def test_invalid_3rd_arg():
    res = subprocess.run(f"{PROG} show invalid_arg",
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         text=True)
    assert "show usage" in res.stderr
    assert res.returncode == 1
