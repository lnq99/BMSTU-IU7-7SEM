from init import ALPHABET, alphabet_shuffle


class Rotor:
    def __init__(self, mapping=None, alphabet=ALPHABET, offset=0):
        if not mapping:
            mapping = alphabet_shuffle(alphabet)
        self.init_alphabet = alphabet
        self.init_offset = offset
        self.reset()
        self.mapping_str = mapping
        self.forward_mapping = dict(zip(self.alphabet, mapping))
        self.backward_mapping = dict(zip(mapping, self.alphabet))

    def reset(self):
        self.rotations = 0
        self.alphabet = self.init_alphabet
        self.rotate(self.init_offset)

    def rotate(self, step=1):
        self.alphabet = self.alphabet[step:] + self.alphabet[:step]
        self.rotations = (self.rotations + step) % len(self.alphabet)
        return self.rotations

    def forward(self, char):
        return self.forward_mapping[char]

    def backward(self, char):
        return self.backward_mapping[char]

    def next(self, index, back=False):
        c = self.alphabet[index]
        c = self.backward(c) if back else self.forward(c)
        return self.alphabet.index(c)

    def __str__(self) -> str:
        return f'Alpha.:\t{self.init_alphabet}\n' \
            f'Map:\t{self.mapping_str[-self.rotations:]}{self.mapping_str[:-self.rotations]}\n' \
            f'Offset:\t{self.rotations}\n'
