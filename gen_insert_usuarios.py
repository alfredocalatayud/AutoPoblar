from faker import Faker
from progress.bar import Bar
from os import remove, path
import secrets, string, random, os, time

fake = Faker('es_ES')

if path.exists('usuarios.sql'):
	remove('usuarios.sql')

f = open("usuarios.sql", "x")
f = open("usuarios.sql", "a")

fichero_nifs = open("nifs.txt")
nifs = fichero_nifs.readlines()


bar = Bar('Procesando:', max=len(nifs))
f.write('insert into usuario (nif, mail, contrasenya, telefono, activo) values ')
i = 0

for nif in nifs:
	bar.next() 	

	f.write('(\'' + nif.replace("\n", "") + '\', \'' + fake.unique.email() + '\', \'' + fake.password() + '\', \'' + fake.phone_number() + '\', ' + str(random.randint(0, 1)) + ')')
	
	i += 1

	if i % 1000 == 0:
		f.write(';\n')
		if i < len(nifs):
			f.write('insert into usuario (nif, mail, contrasenya, telefono, activo) values ')

	elif i < len(nifs):
		f.write(',\n')

	
bar.finish()		
f.close();	
