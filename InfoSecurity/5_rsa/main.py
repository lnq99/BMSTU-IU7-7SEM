from rsa import RSA

if __name__ == '__main__':

    rsa = RSA(256)

    rsa.encrypt_file('data.txt', 'encrypt.txt')
    rsa.decrypt_file('encrypt.txt', 'decrypt.txt')
