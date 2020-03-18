#!/usr/bin/env kickoff

import sys

def _verbose_command_wrapper(cmd, args, kwargs):
    print(f"Executing {cmd.__name__!r} against args={args!r}, kwargs={kwargs!r}")
    ret = cmd(*args, **kwargs)
    print(f"Done with {cmd.__name__!r}, result: {ret!r}")

def average(*items: dict(type=int)):
    print(f"I'm calculating average")
    return sum(items) / len(items)

if __name__ == "__kickoff__":
    import kickoff
    kickoff.config.command_wrapper = _verbose_command_wrapper

