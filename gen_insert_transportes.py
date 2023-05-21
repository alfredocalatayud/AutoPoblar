from faker import Faker
from progress.bar import Bar
from os import remove, path
import secrets, string, random, os, time

fake = Faker('es_ES')

K_SALIDA = 'transportes.sql'
K_NIFS = "nifs.txt"
K_TRANSPORTES = "transportes.txt"
K_INSERT = 'insert into transporte (nif, nombre) values '
K_DIV_INSERT = 20
K_N_INSERT = 20

if path.exists(K_SALIDA):
	remove(K_SALIDA)
	
	
f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

fichero_nifs = open(K_NIFS)
nifs = fichero_nifs.readlines()

fichero_transportes = open(K_TRANSPORTES)
transportes = fichero_transportes.readlines()

bar = Bar('Generando transportes:', max=K_N_INSERT)

f.write(K_INSERT)

i=0
j=1
k = 600

for transporte in transportes:
	bar.next() 
	
	f.write('(\'' + nifs[k].replace("\n", "") + '\', \'' + transporte.replace("\n", "") + '\')')
	
	i+=1 
	j+=1
	k+=1

	if i % K_DIV_INSERT == 0:
		f.write(';\n')
		if i < K_N_INSERT:
			f.write(K_INSERT)

	elif i < K_N_INSERT:
		f.write(',\n')
	
bar.finish()		
f.close();	
