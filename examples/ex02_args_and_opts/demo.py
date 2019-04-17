#!/usr/bin/env kickoff

"""Demonstrates misc types of arguments and options"""

def greet(*names, greeting='Hello'):

    if names:
        for name in names:
            print(f"{greeting} {name}!")
    else:
        print("Nothing to do")


def sign_up(*,
            user:   dict(prompt=True),
            passwd: dict(prompt=True, hide_input=True)):

    if len(passwd) < 6:
        print(f"{user}, this password is too weak")
    else:
        print(f"That's a great password {user}!")


def divide(divident: dict(type=int),
           divisor=1,
           *,
           integer : dict(alias='-i', help='Apply floor to the result') =False):

    if integer:
        quotient = divident // divisor
    else:
        quotient = divident / divisor

    print(f"Your quotient is {quotient}")

