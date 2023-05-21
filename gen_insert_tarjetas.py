from faker import Faker
from progress.bar import Bar
from os import remove, path
from datetime import date, time, datetime
import secrets, string, random, os, time

fake = Faker('es_ES')

K_SALIDA = 'tarjetas.sql'
K_NIFS = "nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into tarjeta_bancaria (numero, titular, cvv, fecha_caducidad, nif_cliente) values '
K_DIV_INSERT = 100
K_N_INSERT = 200

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
    
	numero = str(fake.unique.credit_card_number(card_type = 'visa'))
	titular = fake.name()
	cvv = str(fake.credit_card_security_code(card_type = 'visa'))
	fecha_caducidad = str(fake.date_between(fecha_inicio, fecha_fin))
	nif_cliente = nifs[i+400].replace("\n", "")
	
	
	f.write('(\'' + numero + '\', \'' + titular + '\', \'' + cvv + '\', \'' + fecha_caducidad + '\', \'' + nif_cliente + '\')')
	
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
