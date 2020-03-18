#!/usr/bin/env kickoff

import time

def sleep(t: dict(type=int)):
    time.sleep(t)

class Say:
    from say import hi, bye

class calc:
    from calc import add, mul, pro

if __name__ == "__kickoff__":
    import kickoff
    kickoff.config.accept_imported = True
    kickoff.config.blacklist = [sleep]


