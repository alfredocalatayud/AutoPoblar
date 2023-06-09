from faker import Faker
from progress.bar import Bar
from os import remove, path

K_SALIDA = './SQL/direcciones.sql'
K_NIFS = "./static/nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into direccion (id, nif_usuario, calle, numero, puerta, localidad, codigo_postal, pais) values '
K_VALUES = "({}, AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)), '{}', '{}', '{}', '{}', '{}', '{}')"
K_DIV_INSERT = 2000

def main():
	fake = Faker('es_ES')

	if path.exists(K_SALIDA):
		remove(K_SALIDA)
		
		
	f = open(K_SALIDA, "x", encoding="utf-8")
	f = open(K_SALIDA, "a", encoding="utf-8")

	fichero_nifs = open(K_NIFS, encoding="utf-8")
	nifs = fichero_nifs.readlines()

	bar = Bar('Generando direcciones:', max=len(nifs))
	f.write(K_INSERT)

	i=0
	j=1

	for nif in nifs:
		bar.next() 

		id = str(j)
		nif_usuario = nif.replace("\n", "")
		calle = fake.street_name()
		numero = fake.building_number()
		puerta = fake.bothify(text = '##??', letters=K_LETRAS)	
		localidad = fake.city()
		codigo_postal = fake.postcode()
		pais = fake.country().replace('ô', 'o').replace('\'','')

		f.write(K_VALUES.format(id, nif_usuario, calle, numero, puerta, localidad, codigo_postal, pais))
		
		i+=1 
		j+=1

		if i % K_DIV_INSERT == 0 or i == K_DIV_INSERT:
			f.write(';\n')
			if i < len(nifs):
				f.write(K_INSERT)
		
		elif i < len(nifs):
			f.write(',\n')
		
	bar.finish()		
	f.close();	
