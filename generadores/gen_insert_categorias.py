from faker import Faker
from progress.bar import Bar
from os import remove, path
import requests

from utiles import imagenurl as url

K_SALIDA = './SQL/categorias.sql'
K_NIFS = "./static/categorias.txt"
K_INSERT = "insert into categoria (id, nombre, categoria_padre, imagen) values "
K_VALUES = "({}, '{}', {}, '{}')"
K_DIV_INSERT = 190

def main():
    driver = url.init_driver()
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

        f.write(K_VALUES.format(str(j), nifs[i].replace("\n", ""), "NULL", url.get_images_from_google(driver, 0, 1, nifs[i].replace("\n", ""))))

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
        f.write(K_VALUES.format(str(j), nifs[i].replace("\n", ""), str(k), url.get_images_from_google(driver, 0, 1, nifs[i].replace("\n", ""))))

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
    driver.close()
    f.close();	
