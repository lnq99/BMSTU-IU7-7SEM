from config import *
from utils import *


def feistel(msg: int, subkey: int):
    m = permute(msg, E, 32)
    z = m ^ subkey

    res = 0

    for i in range(8):
        zi = z >> ((7-i)*6) & 63
        x = (zi >> 5 << 1) + (zi & 1)
        y = (zi >> 1) & 0xf
        res <<= 4
        # print(int_to_bin_str(zi))
        # print(x, y, S_BOX[i][x][y])
        res += S_BOX[i][x][y]

    return permute(res, P, 32)


class DES:

    def __init__(self, hex_key, trace=False):
        self.key = int(hex_key, 16)
        self.trace = trace
        print(self)
        self.create_keys()

    def create_keys(self):
        c0 = permute(self.key, C0, 64)
        d0 = permute(self.key, D0, 64)

        if self.trace:
            print(f'C0: {int_to_bin_str(c0, 28)}')
            print(f'D0: {int_to_bin_str(d0, 28)}')
            print()

        self.subkeys = []

        for i in range(16):
            c0 = rotate_left(c0, SHIFT[i], 28)
            d0 = rotate_left(d0, SHIFT[i], 28)
            self.subkeys.append(permute((c0 << 28)+d0, CP, 56))

        if self.trace:
            for i in range(16):
                print(
                    f'Subkey {i+1: >2}: {int_to_bin_str(self.subkeys[i], 48)}')
            print()

    @staticmethod
    def f_en(l, r, key): return (r, l ^ feistel(r, key))

    @staticmethod
    def f_de(l, r, key): return (r ^ feistel(l, key), l)

    def en_de_crypt(self, block, encrypt=True):
        if encrypt:
            f = self.f_en
            sequence = range(16)
        else:
            f = self.f_de
            sequence = range(15, -1, -1)

        res = permute(block, IP, 64)
        l = res >> 32
        r = res & 0xffffffff

        if not encrypt:
            l, r = r, l

        if self.trace:
            print('In: ', int_to_bin_str(l, 32), '\t', int_to_bin_str(r, 32))

        for i in sequence:
            l, r = f(l, r, self.subkeys[i])
            if self.trace:
                print(f'{i:2}: ', int_to_bin_str(l, 32),
                      '\t', int_to_bin_str(r, 32))

        if encrypt:
            l, r = r, l

        res = (l << 32) + r
        res = permute(res, IP_INV, 64)
        if self.trace:
            print()
            if encrypt:
                print(f"'{int_to_ascii(block)}' -> {int_to_hex_str(res, 16)}")
            else:
                print(f"{int_to_hex_str(block, 16)} -> '{int_to_ascii(res)}'")
            print()
        return res

    def encrypt(self, text):
        text = text.encode('ascii')
        l = len(text)
        res = ''
        for i in range(0, l, 8):
            j = i
            s = 0
            while j < i+8 and j < l:
                s <<= 8
                s += text[j]
                j += 1
            r = self.en_de_crypt(s)
            res += int_to_hex_str(r, 16)
        return res

    def decrypt(self, text):
        l = len(text)
        res = ''

        for i in range(0, l, 16):
            s = int(text[i:i+16], 16)
            # print(f"'{text[i:i+16]}'")
            r = self.en_de_crypt(s, False)
            res += bytearray.fromhex(hex(r)[2:]).decode()
        return res

    def __str__(self) -> str:
        return f'KEY: {int_to_bin_str(self.key, 64)}\n'
