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

	while i < K_N_INSERT:
		bar.next() 
		
		id = str(j)
		calificacion = str(random.randint(1,5))
		titulo = fake.text(max_nb_chars=10)
		cuerpo = fake.text(max_nb_chars=200)
		respuesta = 'NULL'
		fecha = str(fake.date_between(fecha_inicio, fecha_fin))
		nif_cliente = nifs[random.randint(400, 599)].replace("\n", "")
		id_producto = str(random.randint(1, 190))

		# f.write('(' + str(j) + ', ' + calificacion + ', \'' + titulo + '\', \'' + cuerpo + '\', ' + respuesta + ', \'' + fecha + ', \'' + nif_cliente + '\', ' + id_producto + ')')
		f.write(K_VALUES.format(id, calificacion, titulo, cuerpo, respuesta, fecha, nif_cliente, id_producto))
		
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
