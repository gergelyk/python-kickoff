#!/usr/bin/env kickoff
from kickoff.types import HEXDEC
from enum import IntEnum

class Animal(IntEnum):
    dog   = 0x10
    pig   = 0x20
    snake = 0x22
    cow   = 0x44

def accept_enum(val = Animal.pig):
    """Accept value of Animal specified either by name or by integer in decimal or hexadecimal notation"""
    print(f"{val!s} = 0x{val:x} = {val:d}")

def accept_int(val: dict(type=HEXDEC)):
    """Accept an integer in either decimal or hexadecimal notation"""
    print(f"0x{val:x} = {val:d}")

