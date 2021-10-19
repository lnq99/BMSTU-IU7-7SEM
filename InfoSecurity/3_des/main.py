from des import DES

SEP = '='*76+'\n'

if __name__ == '__main__':

    hex_key = '12ab34ef56cd7809'
    des = DES(hex_key, trace=True)

    plain_text = 'DES encr   yptio n '
    # plain_text = 'DES encryption'

    cipher_text = des.encrypt(plain_text)
    print(SEP)
    decrypt_text = des.decrypt(cipher_text)
    print(SEP)

    print(cipher_text)
    print(decrypt_text)
    print(plain_text == decrypt_text)


# Reference
# https://www.youtube.com/watch?v=Sy0sXa73PZA
# padding PKCS #7
