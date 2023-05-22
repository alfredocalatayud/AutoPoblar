from faker import Faker
from progress.bar import Bar
from os import remove, path
import random

K_SALIDA = './SQL/productos.sql'
K_CATEGORIAS = "./static/categorias.txt"
K_NIFS = "./static/nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into producto (id, nombre, descripcion, id_categoria, nif_vendedor, precio, costes_envio, iva, stock, plazo_devolucion, dimensiones, peso, url_imagen, restric_edad, activo, relevancia) values '
K_VALUES = "({}, '{}', '{}', {}, '{}', {}, {}, {}, {}, {}, '{}', {}, '{}', {}, {}, {})"
K_DIV_INSERT = 190
K_N_INSERT = 190

def main():
	fake = Faker('es_ES')

	ivas = [0.05, 0.10, 0.21]
	restricciones = [12, 16, 18]

	if path.exists(K_SALIDA):
		remove(K_SALIDA)
		
		
	f = open(K_SALIDA, "x", encoding="utf-8")
	f = open(K_SALIDA, "a", encoding="utf-8")

	fichero_nifs = open(K_NIFS, encoding="utf-8")
	nifs = fichero_nifs.readlines()

	fichero_categorias = open(K_CATEGORIAS, encoding="utf-8")
	productos = fichero_categorias.readlines()

	bar = Bar('Generando productos:', max=K_N_INSERT)
	f.write(K_INSERT)
	i=0
	j=1

	my_width = 500
	my_height = 1024

	for producto in productos:
		bar.next() 
		
		id = str(j)
		descripcion = fake.text(max_nb_chars=50)
		categoria = str(random.randint(1,100))
		vendedor = nifs[random.randint(200,399)]
		precio = round(random.uniform(1.00, 200.00), 2)
		costes_envio = round(random.uniform(1.00, 10.00), 2)
		iva = ivas[random.randint(0,2)]
		stock = str(random.randint(0, 10000))
		plazo_devolucion = str(random.randint(30,90))
		dimensiones = str(random.randint(1,100)) + 'x' + str(random.randint(1,100)) + 'x' + str(random.randint(1,100))
		peso = str(round(random.uniform(1.00, 200.00), 2))
		url_imagen = fake.image_url(placeholder_url="https://loremflickr.com/{}/{}/food".format(my_width,my_height))
		restric_edad = str(restricciones[random.randint(0,2)])
		activo = str(random.randint(0,1))
		relevancia = str(random.randint(0,100))
		
		# f.write('(' + str(j) + ', \'' + producto.replace("\n", "") + '\', \'' + descripcion + '\', ' + str(categoria) + ', \'' + vendedor.replace("\n", "") + '\', ' + str(precio) + ', ' + str(costes_envio) + ', ' + \
		#  				str(iva) + ', ' + str(stock) + ', ' +str(stock) + ', \'' + dimensiones + '\', ' + str(peso) + ', \'' + url_imagen + '\', ' + str(restric_edad) + ', ' + str(activo) + ', ' + str(relevancia) + ')')
		f.write(K_VALUES.format(id, producto.replace("\n", ""), descripcion, categoria, vendedor.replace("\n", ""), str(precio), str(costes_envio), str(iva), stock, plazo_devolucion, dimensiones, peso, url_imagen, restric_edad, activo, relevancia))
		
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
