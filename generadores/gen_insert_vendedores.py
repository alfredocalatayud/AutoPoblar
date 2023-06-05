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
K_VALUES = "(AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)), '{}', '{}', AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)), {}, '{}')"
K_DIV_INSERT = 200
K_N_PERSONAS = 200

def get_imagen(category):
    # make a request to the Unsplash API to get a random image
	url = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id=1n7sSMtCh8Hs_MrBOjhQ1SygTDA-BJ550UdX3rwLYZQ"
	try:
		data = requests.get(url).json()
		salida = data["urls"]["regular"]
	except:
		salida ="https://images.unsplash.com/photo-1606851181064-b7507b24377c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w0NDgxMTB8MHwxfHJhbmRvbXx8fHx8fHx8fDE2ODU4NzYyNTJ8&ixlib=rb-4.0.3&q=80&w=1080"


	return(salida)


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
		cuenta_bancaria = fake.iban()
		verificado = str(random.randint(0,1))
		logo = get_imagen("market")

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
