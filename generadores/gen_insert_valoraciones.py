from faker import Faker
from progress.bar import Bar
from os import remove, path
from datetime import date
import random

K_SALIDA = './SQL/valoraciones.sql'
K_NIFS = "./static/nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into valoracion (id, calificacion, titulo, cuerpo, respuesta, fecha, nif_cliente, id_producto) values '
K_VALUES = "({}, {}, '{}', '{}', {}, '{}', '{}', {})"
K_DIV_INSERT = 300
K_N_INSERT = 300
K_N_VALORACIONES = 10

def main():
	fake = Faker('es_ES')

	if path.exists(K_SALIDA):
		remove(K_SALIDA)
		
	f = open(K_SALIDA, "x", encoding="utf-8")
	f = open(K_SALIDA, "a", encoding="utf-8")

	fichero_nifs = open(K_NIFS, encoding="utf-8")
	nifs = fichero_nifs.readlines()

	fecha_inicio = date(2021, 1, 1)
	fecha_fin = date(2023, 5, 1)

	bar = Bar('Generando valoraciones:', max=K_N_INSERT)
	f.write(K_INSERT)
	i=0
	j=1
	n_valoraciones = 0

	for nif in nifs:
		if i == K_N_INSERT:
			break
		n_valoraciones+=1
		n_valoracion = random.randint(0,K_N_VALORACIONES)
		valoracion = 0

		for k in range(n_valoracion):
			bar.next()
			id = str(j)
			calificacion = str(random.randint(1,5))
			titulo = fake.text(max_nb_chars=10)
			cuerpo = fake.text(max_nb_chars=200)
			respuesta = 'NULL'
			fecha = str(fake.date_between(fecha_inicio, fecha_fin))
			nif_cliente = nif.replace("\n", "")
			id_producto = str(fake.unique.random_int(1, 190))

			i += 1
			j += 1
			valoracion+=1

			f.write(K_VALUES.format(id, calificacion, titulo, cuerpo, respuesta, fecha, nif_cliente, id_producto))

			if i % K_DIV_INSERT == 0 or i == K_DIV_INSERT or (n_valoraciones == K_N_INSERT and valoracion == n_valoraciones):
				f.write(';\n')
				if i != K_N_INSERT:
					f.write(K_INSERT)
			elif i != K_N_INSERT or valoracion == n_valoraciones:
				f.write(',\n')

			if i == K_N_INSERT:
				break

		fake.unique.clear()
		
	bar.finish()		
	f.close();