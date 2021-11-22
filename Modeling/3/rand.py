import enum
from datetime import datetime
from random import randrange

from scipy.stats import chisquare


class RandomGenerator:
    class Method(enum.Enum):
        Standard = 1
        Table = 2
        LinearCongruential = 3

    def __init__(self, table_path='digits.txt'):
        self.digits = ''
        with open(table_path) as table:
            for line in table:
                self.digits += line[:-1]

        self.table_len = len(self.digits)
        self.seed = int(datetime.now().microsecond)
        self.table_idx = self.seed % self.table_len
        self.table_idx = 0

    def __standard(self, n_digits):
        return randrange(10 ** n_digits)

    # https://en.wikipedia.org/wiki/Linear_congruential_generator
    def __linear_congruential(self, n_digits, modulus=2e31, a=1664525, c=1013904223):
        self.seed = (a * self.seed + c) % modulus
        return int(self.seed / modulus * (10 ** n_digits))

    def __table(self, n_digits):
        num = ''
        for _ in range(n_digits):
            num += self.digits[self.table_idx]
            self.table_idx = (self.table_idx + 1) % self.table_len
        return int(num)

    def rand(self, method: Method, n_digits, n_numbers):
        res = []
        if method == RandomGenerator.Method.Standard:
            res = [self.__standard(n_digits) for _ in range(n_numbers)]
        elif method == RandomGenerator.Method.Table:
            res = [self.__table(n_digits) for _ in range(n_numbers)]
        elif method == RandomGenerator.Method.LinearCongruential:
            res = [self.__linear_congruential(n_digits) for _ in range(n_numbers)]
        return res


class RandomCriteria:
    @staticmethod
    def p_of_chi_square_test(sequence, n_digits):
        d = 10 ** n_digits
        f_obs = [0] * d
        for i in sequence:
            f_obs[i] += 1

        # Got same result: y == chisq
        # y = 0
        # mi = len(sequence) / d
        # for i in range(d):
        #     y += (f_obs[i] - mi) ** 2
        # y /= mi

        chisq, p = chisquare(f_obs)
        return p
