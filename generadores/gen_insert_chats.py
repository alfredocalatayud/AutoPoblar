from faker import Faker
from progress.bar import Bar
from datetime import date
from os import remove, path
import random

K_SALIDA = './SQL/chats.sql'
K_NIFS = "./static/nifs.txt"
K_INSERT = 'insert into chat (id, nif_usuario_1, nif_usuario_2, fecha_inicio, fecha_fin) values '
K_VALUES = "({}, '{}', '{}', '{}', '{}')"
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

	bar = Bar('Generando chats:', max=K_N_PERSONAS)
	f.write(K_INSERT)

	i=0
	j=1

	fecha_inicio = date(2021, 1, 1)
	fecha_fin = date(2023, 5, 1)

	while i < K_N_PERSONAS:
		bar.next() 
		
		fecha_1 = fake.date_between(fecha_inicio, fecha_fin)
		fecha_2 = fake.date_between(fecha_inicio, fecha_fin)

		while fecha_1 >= fecha_2:
			fecha_2 = fake.date_between(fecha_inicio, fecha_fin)

		id = str(j)
		nif_usuario_1 = nifs[random.randint(0,1000)].replace("\n", "")
		nif_usuario_2 = nifs[random.randint(2000,3000)].replace("\n", "")
		f_inicio = str(fecha_1)
		f_fin = str(fecha_2)

		f.write(K_VALUES.format(id, nif_usuario_1, nif_usuario_2, f_inicio, f_fin))
		
		i+=1 
		j+=1

		if i % K_DIV_INSERT == 0:
			f.write(';\n')
			if i < len(nifs) and i < K_DIV_INSERT:
				f.write(K_INSERT)

		elif i < len(nifs):
			f.write(',\n')
		
	bar.finish()		
	f.close();	

