from faker import Faker
from progress.bar import Bar
from os import remove, path
from datetime import date
import random

K_SALIDA = './SQL/listas.sql'
K_NIFS = "./static/nifs.txt"
K_INSERT = 'insert into lista (id, nombre, descripcion, nif_cliente) values '
K_VALUES = "({}, '{}', '{}', AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)))"
K_DIV_INSERT = 2000
K_N_INSERT = 2000

def main():
	fake = Faker('es_ES')

	if path.exists(K_SALIDA):
		remove(K_SALIDA)
		
	f = open(K_SALIDA, "x", encoding="utf-8")
	f = open(K_SALIDA, "a", encoding="utf-8")

	fichero_nifs = open(K_NIFS, encoding="utf-8")
	nifs = fichero_nifs.readlines()


	bar = Bar('Generando listas:', max=K_N_INSERT)
	f.write(K_INSERT)

	i=0
	j=1

	while i < K_N_INSERT:
		bar.next() 
		
		id = str(j)
		nombre = fake.text(max_nb_chars=50)
		descripcion = fake.text(max_nb_chars=200)
		nif_cliente = nifs[random.randint(400,599)].replace("\n", "")
		
		f.write(K_VALUES.format(id, nombre, descripcion, nif_cliente))
		
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
