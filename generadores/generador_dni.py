from faker import Faker
from progress.bar import Bar
from os import remove, path
import os

# Import
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

K_NIFS = 1000000
K_FICHERO_NIFS = './static/nifs.txt'
K_FORMATO_NIF = '########?'
K_LETRAS_NIF = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

SALT = b'\x01\xaet\xd3&\xdb\xfb\x0b\x94f\xc2\xb2\xffm\xf0\x94\xf8K\xb4d\xef%\xf3\xcb\xb7\xaf\xcdH\x92\x81B\xa0' # Para encriptar la key generation
PASSWORD = "abcdefghijklmnopqrstuvwx"


def mi_encripta(line):
    key = PBKDF2(PASSWORD, SALT, dkLen=32)

    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(line, AES.block_size))
    iv = cipher.iv

    return (iv + ciphered_data).decode('latin-1')


def main():
    fake = Faker('es_ES')

    if path.exists(K_FICHERO_NIFS):
        remove(K_FICHERO_NIFS)

    with open(K_FICHERO_NIFS, 'w', encoding='latin-1') as output_file:
        bar = Bar('Creando NIFs:', max=K_NIFS)

        for _ in range(K_NIFS):
            bar.next()
            nif = mi_encripta(fake.unique.bothify(text=K_FORMATO_NIF, letters=K_LETRAS_NIF).encode('utf-8'))

            output_file.write(nif + '\n')

        bar.finish()


if __name__ == "__main__":
    main()
