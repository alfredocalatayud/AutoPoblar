from faker import Faker
from progress.bar import Bar
from os import remove, path
import requests

K_SALIDA = './SQL/categorias.sql'
K_NIFS = "./static/categorias.txt"
K_INSERT = "insert into categoria (id, nombre, categoria_padre, imagen) values "
K_VALUES = "({}, '{}', {}, '{}')"
K_DIV_INSERT = 190

def get_imagen(category):
    url = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id=1n7sSMtCh8Hs_MrBOjhQ1SygTDA-BJ550UdX3rwLYZQ"
    try:
        data = requests.get(url).json()
        salida = data["urls"]["regular"]
    except:
        salida ="https://images.unsplash.com/photo-1606851181064-b7507b24377c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w0NDgxMTB8MHwxfHJhbmRvbXx8fHx8fHx8fDE2ODU4NzYyNTJ8&ixlib=rb-4.0.3&q=80&w=1080"

    return(salida)

def main():
    fake = Faker('es_ES')

    if path.exists(K_SALIDA):
        remove(K_SALIDA)
        
        
    f = open(K_SALIDA, "x", encoding="utf-8")
    f = open(K_SALIDA, "a", encoding="utf-8")

    fichero_nifs = open(K_NIFS, encoding="utf-8")
    nifs = fichero_nifs.readlines()

    bar = Bar('Generando categorías:', max=len(nifs))
    f.write(K_INSERT)

    i=0
    j=1
    k=1
    x=0

    my_width = 500
    my_height = 1024

    while i < 100:
        bar.next()

        # f.write('(' + str(j) + ', \'' + nifs[i].replace("\n", "") + '\', NULL, \'' + 'Todo, aquí irá una imagen' + '\')')
        f.write(K_VALUES.format(str(j), nifs[i].replace("\n", ""), "NULL", get_imagen(nifs[i].replace("\n", ""))))

        i+=1
        j+=1

        if i % K_DIV_INSERT == 0:
            f.write(';\n')
            if i < len(nifs):
                f.write(K_INSERT)

        elif i < len(nifs):
            f.write(',\n')

    while i < K_DIV_INSERT:
        bar.next()

        # f.write('(' + str(j) + ', \'' + nifs[i].replace("\n", "") + '\', ' + str(k) + ', \'' + 'Todo, aquí irá una imagen' + '\')')
        f.write(K_VALUES.format(str(j), nifs[i].replace("\n", ""), str(k), get_imagen(nifs[i].replace("\n", ""))))

        if x % 6 == 0 and x != 0:
            k+=1
        
        i+=1
        j+=1
        x+=1

        if i % K_DIV_INSERT == 0:
            f.write(';\n')
            if i < len(nifs):
                f.write(K_INSERT)

        elif i < len(nifs):
            f.write(',\n')

    bar.finish()		
    f.close();	
