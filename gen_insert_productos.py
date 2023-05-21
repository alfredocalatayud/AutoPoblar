from faker import Faker
from progress.bar import Bar
from os import remove, path
import secrets, string, random, os, time

fake = Faker('es_ES')

K_SALIDA = 'productos.sql'
K_CATEGORIAS = "categorias.txt"
K_NIFS = "nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into producto (id, nombre, descripcion, id_categoria, nif_vendedor, precio, costes_envio, iva, stock, plazo_devolucion, dimensiones, peso, url_imagen, restric_edad, activo, relevancia) values '
K_DIV_INSERT = 190
K_N_INSERT = 190

ivas = [0.05, 0.10, 0.21]
restricciones = [12, 16, 18]

if path.exists(K_SALIDA):
	remove(K_SALIDA)
	
	
f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

fichero_nifs = open(K_NIFS)
nifs = fichero_nifs.readlines()

fichero_categorias = open(K_CATEGORIAS)
productos = fichero_categorias.readlines()

bar = Bar('Generando productos:', max=K_N_INSERT)
f.write(K_INSERT)
i=0
j=1

for producto in productos:
	bar.next() 
	
	categoria = random.randint(1,100)
	vendedor = nifs[random.randint(200,399)]
	descripcion = fake.text(max_nb_chars=50)
	precio = round(random.uniform(1.00, 200.00), 2)
	costes_envio = round(random.uniform(1.00, 10.00), 2)
	iva = ivas[random.randint(0,2)]
	stock = random.randint(0, 10000)
	plazo_devolucion = random.randint(30,90)
	dimensiones = str(random.randint(1,100)) + 'x' + str(random.randint(1,100)) + 'x' + str(random.randint(1,100))
	peso = round(random.uniform(1.00, 200.00), 2)
	url_imagen = 'TODO: url imagen'
	restric_edad = restricciones[random.randint(0,2)]
	activo = random.randint(0,1)
	relevancia = random.randint(0,100)
	
	f.write('(' + str(j) + ', \'' + producto.replace("\n", "") + '\', \'' + descripcion + '\', ' + str(categoria) + ', \'' + vendedor.replace("\n", "") + '\', ' + str(precio) + ', ' + str(costes_envio) + ', ' + \
	 				str(iva) + ', ' + str(stock) + ', ' + str(plazo_devolucion) + ', \'' + dimensiones + '\', ' + str(peso) + ', \'' + url_imagen + '\', ' + str(restric_edad) + ', ' + str(activo) + ', ' + str(relevancia) + ')')
	
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
