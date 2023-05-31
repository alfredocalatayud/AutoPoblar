from faker import Faker
from progress.bar import Bar
from os import remove, path
import os 

# librerías Encriptado
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

K_NIFS = 1000000
K_FICHERO_NIFS = './static/nifs.txt'
K_FORMATO_NIF = '########?'
K_LETRAS_NIF = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

KEY_ENCRYPT = b'\xe3\xdc\x8f\xc1\x16oC0N\xd4\x9023\xa2\x1ej\xbeYu\xcf1\x08k]?\xbc\xeb\xaa=\xc4y\xb5'

def encrypt_line(line, password):
    backend = default_backend()

    key = password  # Utiliza los primeros 32 bytes de la contraseña como clave AES de 256 bits
    iv = os.urandom(16)  # Utiliza los siguientes 16 bytes de la contraseña como IV de 128 bits

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    # Asegúrate de que la línea tenga un tamaño múltiplo del bloque de cifrado
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(line.encode()) + padder.finalize()

    # Encripta la línea y retorna la línea encriptada en formato hexadecimal
    encrypted_line = encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_line.hex()

def main():
	fake = Faker('es_ES')

	if path.exists(K_FICHERO_NIFS):
		remove(K_FICHERO_NIFS)

	with open(K_FICHERO_NIFS, 'w') as output_file:
		bar = Bar('Creando NIFs:', max=K_NIFS)

		for _ in range(K_NIFS):
			bar.next()
			nif = encrypt_line(fake.unique.bothify(text = K_FORMATO_NIF, letters = K_LETRAS_NIF), KEY_ENCRYPT)
			
			output_file.write(nif + '\n')
				
		bar.finish()		
