import sys
sys.path.append('../AutoPoblar')

import mysql.connector

from utiles import encriptar

from datetime import date
from faker import Faker
from progress.bar import Bar
from os import remove, path
import random

K_SALIDA = './SQL/usuarios.sql'
K_NIFS = "./static/nifs.txt"
K_INSERT = 'insert into usuario (nif, mail, contrasenya, telefono, activo, fecha_alta) values '
K_VALUES = "('{}', AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)), SHA('{}'), '{}', {}, '{}')"


BUFFER_SIZE = 8192

def write_buffered(file, data):
    if len(data) > BUFFER_SIZE:
        file.write(data)
    else:
        file.write(data)

def get_len_file(file_name):
    with open(file_name, 'rb') as f:
        return len(f.readlines())

def main():
    fake = Faker('es_ES')

    if path.exists(K_SALIDA):
        remove(K_SALIDA)

    i = 0

    fecha_inicio = date(2022, 1, 1)
    fecha_fin = date(2023, 6, 1)

    # encrypt_file_AES_CBC(KEY_ENCRYPT, K_NIFS, 'SQL/nifs_encriptados.txt')

    len_nifs = get_len_file(K_NIFS)

    with open(K_NIFS, 'r') as input_file, open(K_SALIDA, 'w', encoding='latin-1') as output_file:
        bar = Bar('Generando usuarios:', max=len_nifs)
        output_file.write(K_INSERT)

        buffer = ""

        for i, line in enumerate(input_file):
            bar.next()

            # nif = line[:-2].replace(b'\\n', b'\n')
            # nif = nif.decode('latin-1').replace("'", "''").encode('latin-1')
            nif = line.strip()
            mail = fake.unique.email()
            # mail_encriptado = encriptar.mi_encripta(mail.encode('latin-1'))
            # mail_encriptado = mail_encriptado.decode('latin-1').replace("'", "''").encode('latin-1')
            pwd = fake.password()
            telefono = fake.phone_number()
            activo = str(random.randint(0, 1))
            fecha_alta = str(fake.date_between(fecha_inicio, fecha_fin))

            values = K_VALUES.format(nif, mail, pwd, telefono, activo, fecha_alta)

            # output_file.write(values)
            buffer += values 

            if (i + 1) % 2000 == 0:
                buffer += ';\n'

                write_buffered(output_file, buffer)
                buffer = ''
                if (i + 1) < len_nifs:
                    output_file.write(K_INSERT)
            elif (i + 1) < len_nifs:
                buffer += ',\n'

        if buffer:
            write_buffered(output_file, buffer)

        bar.finish()

if __name__ == "__main__":
    main()