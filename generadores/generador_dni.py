import sys
sys.path.append('../AutoPoblar')

from faker import Faker
from progress.bar import Bar
from os import remove, path
import os

#from utiles import encriptar

K_NIFS = 1000000
K_FICHERO_NIFS = './static/nifs.txt'
K_FORMATO_NIF = '########?'
K_LETRAS_NIF = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    fake = Faker('es_ES')

    if path.exists(K_FICHERO_NIFS):
        remove(K_FICHERO_NIFS)

    with open(K_FICHERO_NIFS, 'w', encoding='latin-1') as output_file:
        bar = Bar('Creando NIFs:', max=K_NIFS)
        primero = 1
        for _ in range(K_NIFS):
            bar.next()
            # nif = encriptar.mi_encripta(fake.unique.bothify(text=K_FORMATO_NIF, letters=K_LETRAS_NIF).encode('latin-1'))
            nif = fake.unique.bothify(text=K_FORMATO_NIF, letters=K_LETRAS_NIF)

            # output_file.write(nif.decode('latin-1').replace('\n', '\\n') + '\n')
            output_file.write(nif + '\n')

        bar.finish()


if __name__ == "__main__":
    main()
