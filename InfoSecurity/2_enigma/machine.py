from rotor import Rotor
from reflector import Reflector
from plugboard import Plugboard
from init import ALPHABET
from typing import List

# x
# x/len(a)
# x/len(a)/len(a)


class Machine:
    def __init__(self, rotors: List[Rotor] = [], reflector: Reflector = None, plugboard: Plugboard = None, alphabet: str = ALPHABET):
        self.alphabet = alphabet
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def reset(self):
        for rotor in self.rotors:
            rotor.reset()

    def encipher(self, text):
        return ''.join(self.encipher_character(c) for c in text)

    def decipher(self, text):
        self.reset()
        return self.encipher(text)

    def encipher_character(self, c):
        c = c.upper()
        if c not in self.alphabet:
            return c

        if self.plugboard:
            c = self.plugboard.exchange(c)

        index = self.alphabet.index(c)

        for rotor in self.rotors:
            index = rotor.next(index)

        if self.reflector:

            c = self.alphabet[index]

            if self.reflector:
                c = self.reflector.reflect(c)

            index = self.alphabet.index(c)

        for rotor in reversed(self.rotors):
            index = rotor.next(index, back=True)

        for rotor in self.rotors:
            if rotor.rotate() != 0:
                break

        c = self.alphabet[index]

        if self.plugboard:
            c = self.plugboard.exchange(c)

        return c

    def __str__(self) -> str:
        rotors_str = '\n'.join(str(i) for i in self.rotors)
        return f'\n=== ROTORS ===\n\n{rotors_str}\n\n' \
            f'== REFLECTOR ==\n\n{str(self.reflector)}\n\n'\
            f'== PLUGBOARD ==\n\n{str(self.plugboard)}\n\n'
