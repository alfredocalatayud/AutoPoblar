from faker import Faker
from progress.bar import Bar
from datetime import date, time, datetime
from os import remove, path
import secrets, string, random, os, time

fake = Faker('es_ES')

K_SALIDA = 'vendedores.sql'
K_NIFS = "nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into vendedor (nif, razon_social, documento_acreditativo_alta, cuenta_bancaria, verificado, logo) values '
K_DIV_INSERT = 200
K_N_PERSONAS = 200

if path.exists(K_SALIDA):
	remove(K_SALIDA)
	
	
f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

fichero_nifs = open(K_NIFS)
nifs = fichero_nifs.readlines()

bar = Bar('Generando direcciones:', max=K_N_PERSONAS)
f.write('set sql_mode = \"NO_AUTO_VALUE_ON_ZERO\";\n')
f.write(K_INSERT)

i=0
j=200

fecha_inicio = date(1950, 1, 1)
fecha_fin = date(2000, 1, 1)

#for nif in nifs:
while j < K_N_PERSONAS*2:
	bar.next() 
	
	
	f.write('(\'' + nifs[j].replace("\n", "") + '\', \'' + fake.company() + '\', \'' + fake.file_name(category='text', extension='pdf') + '\', \'' + fake.iban() + '\', ' + str(random.randint(0,1)) + ', \'' + 'TODO: aquí debe haber una imagen' + '\')')
    # f.write('(\'' + nifs[j].replace("\n", "") + '\', \'' + fake.company() + '\', \'' + fake.iban() + '\', ' + str(random.randint(0,1)) + ', \"' + fake.name() + '\")')
	
	i+=1 
	j+=1

	if i % K_DIV_INSERT == 0:
		if i != K_N_PERSONAS:
			f.write(';\n')
			if i < len(nifs):
				f.write(K_INSERT)

	elif i < len(nifs):
		f.write(',\n')
	
bar.finish()		
f.close();	

