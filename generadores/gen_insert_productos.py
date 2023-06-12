from faker import Faker
from progress.bar import Bar
from os import remove, path
import random
import requests

from utiles import imagenurl as url

K_SALIDA = './SQL/productos.sql'
K_CATEGORIAS = "./static/productos.txt"
K_NIFS = "./static/nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into producto (id, nombre, descripcion, id_categoria, nif_vendedor, precio, costes_envio, iva, stock, plazo_devolucion, dimensiones, peso, url_imagen, restric_edad, activo, relevancia) values '
K_VALUES = "({}, '{}', '{}', {}, AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)), {}, {}, {}, {}, {}, '{}', {}, '{}', {}, {}, {})"
K_DIV_INSERT = 200
K_N_INSERT = 200

# def get_imagen(category):
#     # make a request to the Unsplash API to get a random image
# 	# url = "https://api.unsplash.com/photos/random?query={}&orientation=landscape&client_id=1n7sSMtCh8Hs_MrBOjhQ1SygTDA-BJ550UdX3rwLYZQ".format(category.replace(" ", "")) Robado
# 	url = "https://api.unsplash.com/photos/random?query={}&orientation=landscape&client_id=zY84sTDYD7zGSN8w8KYmk_Id6eP9JZlBVqHA1wiovWI".format(category.replace(" ", "")) # Mio
# 	try:
# 		data = requests.get(url).json()
# 		salida = data["urls"]["regular"]
# 	except:
# 		salida ="https://images.unsplash.com/photo-1606851181064-b7507b24377c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w0NDgxMTB8MHwxfHJhbmRvbXx8fHx8fHx8fDE2ODU4NzYyNTJ8&ixlib=rb-4.0.3&q=80&w=1080"


# 	return(salida)

def main():
	driver = url.init_driver()
	fake = Faker('es_ES')

	ivas = [0.05, 0.10, 0.21]
	restricciones = [0, 5, 12, 16, 18]

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

	for producto in productos:
		bar.next() 
		
		id = str(j)
		nombre = producto.replace("\n", "")
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
		url_imagen = url.get_images_from_google(driver, 0, 1, nombre)
		restric_edad = str(restricciones[random.randint(0,2)])
		activo = str(random.randint(0,1))
		relevancia = str(random.randint(0,100))
		
		f.write(K_VALUES.format(id, nombre, descripcion, categoria, vendedor.replace("\n", ""), str(precio), str(costes_envio), str(iva), stock, plazo_devolucion, dimensiones, peso, url_imagen, restric_edad, activo, relevancia))
		
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
	driver.close()


if __name__ == "__main__":
    main()