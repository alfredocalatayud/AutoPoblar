from faker import Faker
from progress.bar import Bar
from datetime import date
from os import remove, path

K_SALIDA = './SQL/empleados.sql'
K_NIFS = "./static/nifs.txt"
K_INSERT = 'insert into empleado (nif, nombre, apellidos, fecha_nacimiento, numero_seguridad_social, cargo_empresa) values '
K_VALUES = "('{}', '{}', '{}', '{}', '{}', '{}')"
K_DIV_INSERT = 200
K_N_PERSONAS = 200


def main():
	fake = Faker('es_ES')

	if path.exists(K_SALIDA):
		remove(K_SALIDA)
		
		
	f = open(K_SALIDA, "x", encoding="utf-8")
	f = open(K_SALIDA, "a", encoding="utf-8")

	fichero_nifs = open(K_NIFS, encoding="utf-8")
	nifs = fichero_nifs.readlines()

	bar = Bar('Generando empleados:', max=K_N_PERSONAS)
	f.write(K_INSERT)

	i=0
	j=0

	fecha_inicio = date(1950, 1, 1)
	fecha_fin = date(2000, 1, 1)

	#for nif in nifs:
	while j < K_N_PERSONAS:
		bar.next() 

		nif = nifs[j].replace("\n", "")
		nombre = fake.first_name()
		apellidos = fake.last_name() + ' ' + fake.last_name()
		fecha_nacimiento = str(fake.date_between(fecha_inicio, fecha_fin))
		numero_seguridad_social = fake.bban()
		cargo_empresa = fake.job()
		
		f.write(K_VALUES.format(nif, nombre, apellidos, fecha_nacimiento, numero_seguridad_social, cargo_empresa))
		
		i+=1 
		j+=1

		if i % K_DIV_INSERT == 0 or i == K_DIV_INSERT:
			f.write(';\n')
			if i < len(nifs) and i < K_N_PERSONAS:
				f.write(K_INSERT)
		
		elif i < len(nifs):
			f.write(',\n')
		
	bar.finish()		
	f.close();	
