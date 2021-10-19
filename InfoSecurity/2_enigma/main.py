from machine import Machine
from rotor import Rotor
from reflector import Reflector
from plugboard import Plugboard


if __name__ == '__main__':

    rotors = [
        Rotor(),
        Rotor(),
        Rotor(),
    ]

    reflector = Reflector()

    plugboard = Plugboard('AB DT QL EZ XY')

    machine = Machine(rotors, reflector, plugboard)

    print(machine)

    text = 'Enigma test'
    en = machine.encipher(text)
    de = machine.decipher(en)

    print(en)
    print(de)
    print(text.upper() == de)
