from faker import Faker
from progress.bar import Bar
from datetime import date, time, datetime
from os import remove, path
import secrets, string, random, os, time

K_SALIDA = './SQL/vendedores.sql'
K_NIFS = "./static/nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into vendedor (nif, razon_social, documento_acreditativo_alta, cuenta_bancaria, verificado, logo) values '
K_VALUES = "('{}', '{}', '{}', '{}', {}, '{}')"
K_DIV_INSERT = 200
K_N_PERSONAS = 200

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
