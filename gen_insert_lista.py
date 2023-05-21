from faker import Faker
from progress.bar import Bar
from os import remove, path
from datetime import date, time, datetime
import secrets, string, random, os, time

fake = Faker('es_ES')

K_SALIDA = 'listas.sql'
K_NIFS = "nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into lista (id, nombre, descripcion, nif_cliente) values '
K_DIV_INSERT = 2000
K_N_INSERT = 2000

if path.exists(K_SALIDA):
	remove(K_SALIDA)
	
	
f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

fichero_nifs = open(K_NIFS)
nifs = fichero_nifs.readlines()

fecha_inicio = date(2023, 1, 1)
fecha_fin = date(2031, 1, 1)

bar = Bar('Generando productos:', max=K_N_INSERT)
f.write(K_INSERT)

i=0
j=1

while i < K_N_INSERT:
	bar.next() 
    
	nombre = fake.text(max_nb_chars=50)
	descripcion = fake.text(max_nb_chars=200)
	nif_cliente = nifs[random.randint(400,599)].replace("\n", "")
	
	
	f.write('(' + str(j) + ', \'' + nombre + '\', \'' + descripcion + '\', \'' + nif_cliente + '\')')
	
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
