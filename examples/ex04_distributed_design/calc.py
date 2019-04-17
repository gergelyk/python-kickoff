

def add(x: dict(type=float), y: dict(type=float)):
    return x + y

def mul(x: dict(type=float), y: dict(type=float)):
    return x * y

class pro:

    def factorial(x: dict(type=int)):
        if x == 0:
            return 1
        else:
            return x * pro.factorial(x-1)

    def gcd(x: dict(type=int), y: dict(type=int)):
        while y != 0:
            (x, y) = (y, x % y)
        return x
