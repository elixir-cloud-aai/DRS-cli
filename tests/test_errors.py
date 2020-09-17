"""Test file for errors.py"""
import sys

from drs_cli.errors import exception_handler


EXPECTED_MSG = ""


def test_exception_handler():
    exception_handler(_type=str,
                      value=BaseException(),
                      traceback=sys.exc_info()[2])

    exception_handler(_type=str,
                      value=ZeroDivisionError("Divide by zero not allowed"),
                      traceback=sys.exc_info()[2])
    assert sys.excepthook is exception_handler
