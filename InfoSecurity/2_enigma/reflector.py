import random
from init import ALPHABET


class Reflector:
    def __init__(self, mapping=None, alphabet=ALPHABET):
        if not mapping:
            n = len(alphabet)
            a = list(alphabet)
            l = [''] * n

            # alphabet = ['a', 'b', 'c']
            # a = ['b']
            # 2
            # l = ['c', '', 'a']
            # set (abcdef)

            # l = ['', ]

            # [c]
            for i in range(n):
                if l[i] == '':
                    l[i] = alphabet[i]
                    while l[i] == alphabet[i]:
                        l[i] = random.choice(a)

                    j = alphabet.index(l[i])
                    l[j] = alphabet[i]
                    a.remove(l[i])
                    a.remove(l[j])
            mapping = ''.join(l)

        self.mapping_str = mapping
        self.mapping = dict(zip(alphabet, mapping))
        self.alphabet = alphabet

        for x, y in self.mapping.items():
            if x == y:
                raise ValueError(f'Reflect same character {x}->{y}')
            if x != self.mapping[y]:
                raise ValueError(f'{x}-->{y} but {y}-/->{x}')

    def reflect(self, char):
        return self.mapping[char]

    def __str__(self) -> str:
        return f'Alpha.:\t{self.alphabet}\n' \
            f'Map:\t{self.mapping_str}\n'
