from math import ceil, sqrt
from random import randint, getrandbits


def gcd(a, b):
    if a < b:
        a, b = b, a
    if b < 0:
        raise ValueError(f'{b} < 0')
    while b:
        a, b = b, a % b
    return a


def gcd_extend(a, b):
    '''
    ax + by = gcd(a,b)
    '''
    # if a < b or b < 0:
    #     raise ValueError

    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b:
        r = a % b
        if r == 0:
            break
        q = a // b
        a, b = b, r

        x0, x1 = x1, x0-x1*q
        y0, y1 = y1, y0-y1*q

    return b, x1, y1


def mod_inverse(a, m):
    '''
    ax = 1 (mod m)
    '''
    g, x, _ = gcd_extend(a, m)
    if g != 1:
        return -1
    return (x % m + m) % m


def is_prime(n: int) -> bool:
    if n > 1:
        s = ceil(sqrt(n))
        for i in range(2, s+1):
            if n % i == 0:
                break
        else:
            return True

    return False


def miller_rabin_test(n: int, rounds: int = 1) -> bool:
    if n == 2:
        return True
    if n % 2 == 0 or n < 2:
        return False
    t = n - 1
    s = 0

    while t % 2 == 0:
        t >>= 1
        s += 1

    for _ in range(rounds):
        a = randint(1, n-2)
        b = pow(a, t, n)

        if b == 1 or b == n - 1:
            break

        for _ in range(s-1):
            b = pow(b, 2, n)
            if b == n - 1:
                break
        else:
            return False

    return True


def rand_prime(bits):
    while True:
        # first and last bit = 1
        p = (1 << (bits-1)) + 1 + (getrandbits(bits-2) << 1)
        if miller_rabin_test(p, 10):
            return p
