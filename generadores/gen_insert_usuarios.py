from datetime import date
from faker import Faker
from progress.bar import Bar
from os import remove, path
import random

K_SALIDA = './SQL/usuarios.sql'
K_NIFS = "./static/nifs.txt"
K_INSERT = 'insert into usuario (nif, mail, contrasenya, telefono, activo, fecha_alta) values '
K_VALUES = "('{}', '{}', '{}', '{}', {}, '{}')"

def main():
	fake = Faker('es_ES')

	if path.exists(K_SALIDA):
		remove(K_SALIDA)

	f = open(K_SALIDA, "x", encoding="utf-8")
	f = open(K_SALIDA, "a", encoding="utf-8")

	fichero_nifs = open(K_NIFS, encoding="utf-8")
	nifs = fichero_nifs.readlines()


	bar = Bar('Generando usuarios:', max=len(nifs))
	f.write(K_INSERT)
	i = 0

	fecha_inicio = date(2022, 1, 1)
	fecha_fin = date(2023, 6, 1)

	for nif in nifs:
		bar.next() 	
		
		mail = fake.unique.email()
		pwd = fake.password()
		telefono = fake.phone_number()
		activo = str(random.randint(0, 1))
		fecha_alta = str(fake.date_between(fecha_inicio, fecha_fin))

		# f.write('(\'' + nif.replace("\n", "") + '\', \'' + fake.unique.email() + '\', \'' + fake.password() + '\', \'' + fake.phone_number() + '\', ' + str(random.randint(0, 1)) + ')')
		f.write(K_VALUES.format(nif.replace("\n", ""), mail, pwd, telefono, activo, fecha_alta))
		
		i += 1

		if i % 2000 == 0:
			f.write(';\n')
			if i < len(nifs):
				f.write(K_INSERT)

		elif i < len(nifs):
			f.write(',\n')

		
	bar.finish()		
	f.close();	
