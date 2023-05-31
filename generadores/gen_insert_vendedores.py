from faker import Faker
from progress.bar import Bar
from datetime import date, time, datetime
from os import remove, path
import secrets, string, random, os, time

# librerías Encriptado
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

K_SALIDA = './SQL/vendedores.sql'
K_NIFS = "./static/nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into vendedor (nif, razon_social, documento_acreditativo_alta, cuenta_bancaria, verificado, logo) values '
K_VALUES = "('{}', '{}', '{}', '{}', {}, '{}')"
K_DIV_INSERT = 200
K_N_PERSONAS = 200

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

	bar = Bar('Generando vendedores:', max=K_N_PERSONAS)
	f.write(K_INSERT)

	i=0
	j=200

	my_width = 500
	my_height = 1024

	fecha_inicio = date(1950, 1, 1)
	fecha_fin = date(2000, 1, 1)

	#for nif in nifs:
	while j < K_N_PERSONAS*2:
		bar.next()

		nif = nifs[j].replace("\n", "")
		razon_social = fake.unique.company()
		documento_acreditativo_alta = fake.file_name(category='text', extension='pdf')
		cuenta_bancaria = encrypt_line(fake.iban(), KEY_ENCRYPT)
		verificado = str(random.randint(0,1))
		logo = fake.image_url(placeholder_url="https://loremflickr.com/{}/{}/business".format(my_width,my_height))
		
		# f.write('(\'' + nifs[j].replace("\n", "") + '\', \'' + fake.company() + '\', \'' + fake.file_name(category='text', extension='pdf') + '\', \'' + fake.iban() + '\', ' + str(random.randint(0,1)) + ', \'' + 'TODO: aquí debe haber una imagen' + '\')')
		f.write(K_VALUES.format(nif, razon_social, documento_acreditativo_alta, cuenta_bancaria, verificado, logo))
		
		i+=1 
		j+=1

		if i % K_DIV_INSERT == 0:
			if i != K_N_PERSONAS:
				f.write(';\n')
				if i < len(nifs):
					f.write(K_INSERT)

		elif i < len(nifs):
			f.write(',\n')

	f.write(';\n')
	bar.finish()		
	f.close();	
