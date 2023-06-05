from faker import Faker
from progress.bar import Bar
from os import remove, path

K_SALIDA = './SQL/transportes.sql'
K_NIFS = "./static/nifs.txt"
K_TRANSPORTES = "./static/transportes.txt"
K_INSERT = 'insert into transporte (nif, nombre) values '
K_VALUES = "('{}', '{}')"
K_DIV_INSERT = 20
K_N_INSERT = 20

def main():
	fake = Faker('es_ES')

	if path.exists(K_SALIDA):
		remove(K_SALIDA)
		
		
	f = open(K_SALIDA, "x", encoding="utf-8")
	f = open(K_SALIDA, "a", encoding="utf-8")

	fichero_nifs = open(K_NIFS, encoding="utf-8")
	nifs = fichero_nifs.readlines()

	fichero_transportes = open(K_TRANSPORTES, encoding="utf-8")
	transportes = fichero_transportes.readlines()

	bar = Bar('Generando transportes:', max=K_N_INSERT)

	f.write(K_INSERT)

	i=0
	j=1
	k = 600

	for transporte in transportes:
		bar.next() 

		nif =  nifs[k].replace("\n", "")
		nombre = transporte.replace("\n", "")
		
		f.write(K_VALUES.format(nif, nombre))
		
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