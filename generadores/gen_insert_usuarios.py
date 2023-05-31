from datetime import date
import os
from faker import Faker
from progress.bar import Bar
from os import remove, path
import random

# librerías Encriptado
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

K_SALIDA = './SQL/usuarios.sql'
K_NIFS = "./static/nifs.txt"
K_INSERT = 'insert into usuario (nif, mail, contrasenya, telefono, activo, fecha_alta) values '
K_VALUES = "('{}', '{}', '{}', '{}', {}, '{}')"

KEY_ENCRYPT = b'\xe3\xdc\x8f\xc1\x16oC0N\xd4\x9023\xa2\x1ej\xbeYu\xcf1\x08k]?\xbc\xeb\xaa=\xc4y\xb5'

BUFFER_SIZE = 8192
	
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
			mail = encrypt_line(fake.unique.email(), KEY_ENCRYPT)
			pwd = fake.password()
			telefono = encrypt_line(fake.phone_number(), KEY_ENCRYPT)
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


	# with open('SQL/nifs_encriptados.bin', 'rb') as file:
	# 	encrypted_data = file.read()

	# with open(K_SALIDA, "w", encoding="utf-8", buffering=BUFFER_SIZE) as f:
	# 	bar = Bar('Generando usuarios:', max=len(encrypted_data))
	# 	f.write(K_INSERT)

	# 	buffer = ""

	# 	for i, nif in enumerate(encrypted_data):
	# 		bar.next()

	# 		mail = fake.unique.email()
	# 		pwd = fake.password()
	# 		telefono = fake.phone_number()
	# 		activo = str(random.randint(0, 1))
	# 		fecha_alta = str(fake.date_between(fecha_inicio, fecha_fin))

	# 		values = K_VALUES.format(nif, mail, pwd, telefono, activo, fecha_alta)
	# 		buffer += values

	# 		if (i + 1) % 2000 == 0:
	# 			buffer += ';\n'
	# 			write_buffered(f, buffer)
	# 			buffer = ''
	# 			if (i + 1) < len(nifs):
	# 				f.write(K_INSERT)
	# 		elif (i + 1) < len(nifs):
	# 			buffer += ',\n'

	# 	if buffer:
	# 		write_buffered(f, buffer)

	# 	bar.finish()
	
	# fichero_nifs.close()

if __name__ == "__main__":
	main()