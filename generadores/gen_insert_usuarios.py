from datetime import date
import os
from faker import Faker
from progress.bar import Bar
from os import remove, path
import random

# Import
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

K_SALIDA = './SQL/usuarios.sql'
K_NIFS = "./static/nifs.txt"
K_INSERT = 'insert into usuario (nif, mail, contrasenya, telefono, activo, fecha_alta) values '
K_VALUES = "('{}', '{}', '{}', '{}', {}, '{}')"

SALT = b'\x01\xaet\xd3&\xdb\xfb\x0b\x94f\xc2\xb2\xffm\xf0\x94\xf8K\xb4d\xef%\xf3\xcb\xb7\xaf\xcdH\x92\x81B\xa0'
PASSWORD = "abcdefghijklmnopqrstuvwx"

BUFFER_SIZE = 8192

def mi_encripta(line):
    key = PBKDF2(PASSWORD, SALT, dkLen=32)

    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(line, AES.block_size))
    iv = cipher.iv

    return iv + ciphered_data

def write_buffered(file, data):
    if len(data) > BUFFER_SIZE:
        file.write(data)
    else:
        file.write(data, BUFFER_SIZE)


def main():
    fake = Faker('es_ES')

    if path.exists(K_SALIDA):
        remove(K_SALIDA)

    i = 0

    fecha_inicio = date(2022, 1, 1)
    fecha_fin = date(2023, 6, 1)

    # encrypt_file_AES_CBC(KEY_ENCRYPT, K_NIFS, 'SQL/nifs_encriptados.txt')

    with open(K_NIFS, 'r') as input_file, open(K_SALIDA, 'w') as output_file:
        bar = Bar('Generando usuarios:', max=1000000)
        output_file.write(K_INSERT)

        buffer = ""

        for i, line in enumerate(input_file):
            bar.next()

            nif = line.strip()
            mail = mi_encripta(fake.unique.email().encode('utf-8')).decode()
            pwd = fake.password()
            telefono = mi_encripta(fake.phone_number().encode('utf-8'))
            activo = str(random.randint(0, 1))
            fecha_alta = str(fake.date_between(fecha_inicio, fecha_fin))

            values = K_VALUES.format(nif, mail, pwd, telefono, activo, fecha_alta)

            buffer += values

            if (i + 1) % 2000 == 0:
                buffer += ';\n'

                write_buffered(output_file, buffer)
                buffer = ''
                if (i + 1) < 1000000:
                    output_file.write(K_INSERT)
            elif (i + 1) < 1000000:
                buffer += ',\n'

        if buffer:
            write_buffered(output_file, buffer)

        bar.finish()



