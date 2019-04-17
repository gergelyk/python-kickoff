#!/usr/bin/env kickoff

"""Very simple application"""

def greet(name="World", *, greeting="Hello"):
    """Say hello"""

    print(f"{greeting} {name}!")

