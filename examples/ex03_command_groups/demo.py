#!/usr/bin/env kickoff

import time

def sleep(t: dict(type=int)):
    time.sleep(t)


class say:

    def hi():
        print('hi mate!')

    def bye():
        print('bye mate!')


class calc:

    def add(x: dict(type=float), y: dict(type=float)):
        return x + y

    def mul(x: dict(type=float), y: dict(type=float)):
        return x * y

    class pro:

        def factorial(x: dict(type=int)):
            if x == 0:
                return 1
            else:
                return x * calc.pro.factorial(x-1)

        def gcd(x: dict(type=int), y: dict(type=int)):
            while y != 0:
                (x, y) = (y, x % y)
            return x

