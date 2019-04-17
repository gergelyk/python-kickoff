#!/usr/bin/env kickoff

"""Very simple application"""

def hello(name="World") -> dict(short_help="say hello"):
    """Say hello to the person of selected name"""
    print(f"Hello {name}")


if __name__ == "__kickoff__":
    import kickoff
    kickoff.config.prog_name = "demo"
    kickoff.config.version_option = dict(version='1.2.3')
    kickoff.config.help_option_names = ['-h', '--help']

