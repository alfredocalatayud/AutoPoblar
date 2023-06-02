from faker import Faker
from progress.bar import Bar
from os import remove, path
from datetime import date
import os

# librerías Encriptado
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


K_SALIDA = './SQL/tarjetas.sql'
K_NIFS = "./static/nifs.txt"
K_INSERT = 'insert into tarjeta_bancaria (numero, titular, cvv, fecha_caducidad, nif_cliente) values '
K_VALUES = "('{}', AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)), '{}', '{}', '{}')"
K_DIV_INSERT = 100
K_N_INSERT = 200

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

	if path.exists(K_SALIDA):
		remove(K_SALIDA)
		
		
	f = open(K_SALIDA, "x", encoding="utf-8")
	f = open(K_SALIDA, "a", encoding="utf-8")

	fichero_nifs = open(K_NIFS, encoding="utf-8")
	nifs = fichero_nifs.readlines()

	fecha_inicio = date(2023, 1, 1)
	fecha_fin = date(2031, 1, 1)

	bar = Bar('Generando tarjetas:', max=K_N_INSERT)
	f.write(K_INSERT)

	i=0
	j=1

	while i < K_N_INSERT:
		bar.next() 
		
		numero = encrypt_line(str(fake.unique.credit_card_number(card_type = 'visa')), KEY_ENCRYPT)
		titular = encrypt_line(fake.name(), KEY_ENCRYPT)
		cvv = str(fake.credit_card_security_code(card_type = 'visa'))
		fecha_caducidad = str(fake.date_between(fecha_inicio, fecha_fin))
		nif_cliente = nifs[i+400].replace("\n", "")
		
		
		# f.write('(\'' + numero + '\', \'' + titular + '\', \'' + cvv + '\', \'' + fecha_caducidad + '\', \'' + nif_cliente + '\')')
		f.write(K_VALUES.format(numero, titular, cvv, fecha_caducidad, nif_cliente))
		
		i+=1 
		j+=1

		if i % K_DIV_INSERT == 0:
			f.write(';\n')
			if i < K_N_INSERT:
				f.write(K_INSERT)

		elif i < K_N_INSERT:
			f.write(',\n')
		
	bar.finish()		
	f.close();	
