from faker import Faker
from progress.bar import Bar
from os import remove, path
import secrets, string, random, os, time

K_NIFS = 1000000
K_FICHERO_NIFS = 'nifs.txt'
K_FORMATO_NIF = '########?'
K_LETRAS_NIF = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

fake = Faker('es_ES')

if path.exists(K_FICHERO_NIFS):
	remove(K_FICHERO_NIFS)

f = open(K_FICHERO_NIFS, "x")
f = open(K_FICHERO_NIFS, "a")

bar = Bar('Creando NIFs:', max=K_NIFS)

for _ in range(K_NIFS):
	bar.next()
	nif = fake.unique.bothify(text = K_FORMATO_NIF, letters = K_LETRAS_NIF)
	
	f.write(nif + '\n')
		
bar.finish()		
f.close();	
