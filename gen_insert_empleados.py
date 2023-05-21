from faker import Faker
from progress.bar import Bar
from datetime import date, time, datetime
from os import remove, path
import secrets, string, random, os, time

fake = Faker('es_ES')

K_SALIDA = 'empleados.sql'
K_NIFS = "nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into empleado (nif, nombre, apellidos, fecha_nacimiento, numero_seguridad_social, cargo_empresa) values '
K_DIV_INSERT = 200
K_N_PERSONAS = 200

if path.exists(K_SALIDA):
	remove(K_SALIDA)
	
	
f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

fichero_nifs = open(K_NIFS)
nifs = fichero_nifs.readlines()

bar = Bar('Generando direcciones:', max=K_N_PERSONAS)
f.write(K_INSERT)

i=0
j=0

fecha_inicio = date(1950, 1, 1)
fecha_fin = date(2000, 1, 1)

#for nif in nifs:
while j < K_N_PERSONAS:
	bar.next() 
	
	#f.write('(\'' + nifs[j].replace("\n", "") + '\', \'' + fake.first_name() + '\', \'' + fake.last_name() + ' ' + fake.last_name() + '\', \'' + str(fake.date_between(fecha_inicio, fecha_fin)) + '\', \'' + fake.bban() + '\', \'' + fake.job() + '\')')
	f.write('(\'' + nifs[j].replace("\n", "") + '\', \'' + fake.first_name() + '\', \'' + fake.last_name() + ' ' + fake.last_name() + '\', \'' + str(fake.date_between(fecha_inicio, fecha_fin)) + '\', \'' + fake.bban() + '\', \'' + fake.job() + '\')')
	
	i+=1 
	j+=1

	if i % K_DIV_INSERT == 0:
		f.write(';\n')
		if i < len(nifs):
			f.write(K_INSERT)

	elif i < len(nifs):
		f.write(',\n')
	
bar.finish()		
f.close();	

