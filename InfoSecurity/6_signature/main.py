import random
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


HASH_ALGO = hashes.SHA256()


class CertificationAuthority:

    CertDB = {}

    @classmethod
    def add(cls, public_key, name):
        k = cls.public_key_text(public_key)
        cls.CertDB[k] = name

    @classmethod
    def get(cls, public_key):
        k = cls.public_key_text(public_key)
        if k in cls.CertDB:
            return cls.CertDB[k]
        return 'Unknown'

    @classmethod
    def info(cls):
        print()
        for key, val in cls.CertDB.items():
            cls._print_key(key)
            print(val)
            print()

    @staticmethod
    def public_key_text(public_key):
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    @staticmethod
    def _print_key(key):
        for e in key.splitlines():
            print(e.decode("utf-8"))


class Sender:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()

    def send(self, receiver, message):
        signature = self.sign(message)
        Network.deliver_message(receiver, message, signature, self.public_key)

    def sign(self, message):
        return self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(HASH_ALGO),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            HASH_ALGO
        )


class Receiver:
    def receive(self, message, signature, public_key):
        print('Received:', message.decode('utf-8'), end='\t')
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(HASH_ALGO),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                HASH_ALGO
            )
            sender = CertificationAuthority.get(public_key)
            print('Message verified! from', sender)
        except InvalidSignature:
            print('Wrong signature!')
        except Exception as err:
            print(err)


class Network:
    hacker = Sender()

    @staticmethod
    def deliver_message(receiver, message, signature, public_key):
        r = random.random()
        if r > 0.7:
            receiver.receive(b'Corrupted message', signature, public_key)
        elif r > 0.4:
            Network.hacker.send(receiver, b'Fake message!!!')
        else:
            receiver.receive(message, signature, public_key)


if __name__ == '__main__':

    s = Sender()
    r = Receiver()

    CertificationAuthority.add(s.public_key, 'Bob')

    for _ in range(10):
        s.send(r, b'S send to R 200$')
        print()

    CertificationAuthority.info()


# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
# Diffie-Hellman key exchange
