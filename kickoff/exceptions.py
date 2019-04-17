import sys
import os
from textwrap import dedent
from .logger import log
from contextlib import contextmanager
from .shared import get_config


class EXIT_CODES:
    UNEXPECTED    = 1 # Default that python returns when an exceptions gets to the level
    USAGE_CLICK   = 2
    USAGE_KICKOFF = 3
    USAGE_USER    = 4


class KickoffUsageError(Exception):
    exit_code = EXIT_CODES.USAGE_KICKOFF


class UserErrorRegister:
    _exception = None

    def set_exc(self, exc):
        self._exception = exc

    def is_set(self, exc):
        return exc is self._exception


user_error_register = UserErrorRegister()


def in_dbg_mode():
    """KICKOFF_DEBUG is unset, empty, or '0' -> False, otherwise -> True"""
    val = os.getenv('KICKOFF_DEBUG')
    return bool(val) and val != '0'


def unexpected_error_handler(exc, *, file=sys.stderr, exit_code=EXIT_CODES.UNEXPECTED):
    msg = "Unexpected error occurred, set KICKOFF_DEBUG=1 to see more details"
    print(msg, file=file)
    exit(exit_code)


def simple_error_handler(exc, *, file=sys.stderr, exit_code=EXIT_CODES.USAGE_USER):
    print(f"Error: {exc}", file=file)
    if hasattr(exc, 'exit_code'):
        exit_code = exc.exit_code
    exit(exit_code)


def kickoff_usage_error_handler(exc):
    UsagePrinter.print_usage()
    simple_error_handler(exc)


@contextmanager
def global_exception_guard():
    """ Handle exceptions before passing them to Python interpreter
    """
    try:
        yield
    except Exception as exc:
        if in_dbg_mode():
            error_handler = None
        elif user_error_register.is_set(exc):
            error_handler = get_config().error_handler
        elif isinstance(exc, KickoffUsageError):
            error_handler = kickoff_usage_error_handler
        else:
            error_handler = unexpected_error_handler

        if error_handler:
            error_handler(exc)
        else:
            raise


@contextmanager
def user_exception_guard():
    """ Use user_error_register to keep this in mind that source of the error is in the user's code
    """
    try:
        yield
    except Exception as exc:
        user_error_register.set_exc(exc)
        raise


class UsagePrinter:

    exe_name = 'kickoff'

    @classmethod
    def print_usage(cls):

        print(dedent(f"""
        Turns your Python script or module into an application with decent CLI.

        Usage:
            # Running a script
            {cls.exe_name} PATH[:] COMMAND ... [ARGS ...]

            Note: Semicolon at the end of PATH is required when PATH itself includes semicolons.

            # Running a module
            {cls.exe_name} [PATH]:MODULE COMMAND ... [ARGS ...]

            Note: If PATH is skipped, MODULE is expected to be available in system locations or on PYTHONPATH.

        Examples:
            {cls.exe_name} some\\relative\\location\\myscript.py foo --bar 123
            {cls.exe_name} C:\\some\\absolute\\location\\myscript.py: foo --bar 123
            {cls.exe_name} C:\\some\\absolute\\location:mymodule foo --bar 123
            {cls.exe_name} :re findall "b\\w*d" "beer bear bird bore beard"

        """).strip())
        print()


