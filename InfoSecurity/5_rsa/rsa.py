from algo import *
from math import log2, floor
from random import randint


class RSA:
    def __init__(self, bits=1024):
        self.size = bits // 8
        bits >>= 1
        p = rand_prime(bits)
        while True:
            q = rand_prime(bits)
            if q != p:
                break

        phi = (p - 1) * (q - 1)
        self.n = p * q
        self.size_less_n = floor(log2(self.n)) // 8
        self.e = self._rand_e(phi)
        self.d = self._calc_d(phi, self.e)

        print('p =', p)
        print('q =', q)
        print(self)

    def __str__(self) -> str:
        return f'n = {self.n}\n' \
            f'e = {self.e}\n' \
            f'd = {self.d}\n'

    def encrypt(self, m: bytes):
        m = int.from_bytes(m, 'big')
        c = pow(m, self.e, self.n)
        c = c.to_bytes(self.size, 'big')
        return c

    def decrypt(self, c):
        c = int.from_bytes(c, 'big')
        m = pow(c, self.d, self.n)
        m = m.to_bytes(self.size, 'big').lstrip(b'\x00')
        return m

    def en_de_crypt(self, in_name, out_name, encrypt=True):
        if encrypt:
            size = self.size_less_n
            func = self.encrypt
        else:
            size = self.size
            func = self.decrypt

        with open(in_name, 'rb') as f_in, open(out_name, 'wb') as f_out:
            d = f_in.read()
            l = len(d)

            for i in range(0, l, size):
                s = d[i:i+size]
                c = func(s)
                f_out.write(c)
                print(s)
                print(c)
                print()

    def encrypt_file(self, in_name, out_name):
        self.en_de_crypt(in_name, out_name)

    def decrypt_file(self, in_name, out_name):
        self.en_de_crypt(in_name, out_name, False)

    @staticmethod
    def _rand_e(phi):
        while True:
            e = randint(2, phi-1)
            if gcd(phi, e) == 1:
                return e

    @staticmethod
    def _calc_d(phi, e):
        '''
        ed + kphi = 1
        ed = 1 (mod phi)
        '''
        return mod_inverse(e, phi)
