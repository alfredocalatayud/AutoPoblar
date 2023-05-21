from faker import Faker
from progress.bar import Bar
from os import remove, path
from datetime import date
import secrets, string, random, os, time

fake = Faker('es_ES')

K_SALIDA = 'valoraciones.sql'
K_NIFS = "nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into valoracion (id, calificacion, titulo, cuerpo, respuesta, fecha, nif_cliente, id_producto) values '
K_DIV_INSERT = 300
K_N_INSERT = 300

if path.exists(K_SALIDA):
	remove(K_SALIDA)
	
	
f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

fichero_nifs = open(K_NIFS)
nifs = fichero_nifs.readlines()

fecha_inicio = date(2021, 1, 1)
fecha_fin = date(2023, 5, 1)

bar = Bar('Generando productos:', max=K_N_INSERT)
f.write(K_INSERT)
i=0
j=1

while i < K_N_INSERT:
	bar.next() 
	
	calificacion = str(random.randint(1,5))
	titulo = fake.text(max_nb_chars=10)
	cuerpo = fake.text(max_nb_chars=200)
	respuesta = 'NULL'
	fecha = fake.date_between(fecha_inicio, fecha_fin)
	nif_cliente = nifs[random.randint(400, 599)].replace("\n", "")
	id_producto = str(random.randint(1, 190))

	f.write('(' + str(j) + ', ' + calificacion + ', \'' + titulo + '\', \'' + cuerpo + '\', ' + respuesta + ', \'' + fecha + ', \'' + nif_cliente + '\', ' + id_producto + ')')
	
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
