#!/usr/bin/env kickoff

from click import UsageError, BadOptionUsage
from click_repl import ExitReplException

class CustomError(UsageError):
    exit_code = 10

def custom_error():
    raise CustomError("Something went wrong")

def usage_error():
    raise UsageError("Incorrect usage")

def option_error():
    raise BadOptionUsage("Incorrect option", "What a pity")

def critical_error():
    raise ExitReplException("Critical error")

def division_error():
    123 / 0

if __name__ == "__kickoff__":
    import kickoff
    # Hide call stacks from the user, show only error message
    # This can be canceled by setting KICKOFF_DEBUG=1
    kickoff.config.error_handler = kickoff.simple_error_handler
