import string
import random


ALPHABET = string.ascii_uppercase


def alphabet_shuffle(alphabet):
    return ''.join(random.sample(alphabet, len(alphabet)))
