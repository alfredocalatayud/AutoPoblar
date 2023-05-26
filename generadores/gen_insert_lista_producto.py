from faker import Faker
from progress.bar import Bar
from os import remove, path
import random
import mysql.connector

DB_HOST = 'bbdd.dlsi.ua.es'

K_SALIDA = './SQL/listas_producto.sql'
K_INSERT = 'insert producto_lista (id_producto, id_lista) values '
K_VALUES = "('{}', '{}')"
K_DIV_INSERT = 1500
K_N_PRODUCTOS = 30
K_N_CHATS = 200

def run_query(query, db_user, db_name, db_pass):
    
    conn = mysql.connector.connect(host = DB_HOST, user = db_user, passwd = db_pass, database = db_name)
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8;")
    cursor.execute("SET CHARACTER SET utf8;")
    cursor.execute("SET character_set_connection=utf8;")
    cursor.execute(query)

    salida = cursor.fetchall()

    cursor.close()
    conn.close()

    return salida 

def main(db_user, db_name, db_pass): 
    fake = Faker('es_ES')

    if path.exists(K_SALIDA):
        remove(K_SALIDA)
        
    productos = run_query('SELECT id FROM producto order by id asc;', db_user, db_name, db_pass)
    listas = run_query('SELECT id FROM lista order by id asc;', db_user, db_name, db_pass)

    f = open(K_SALIDA, "x", encoding="utf-8")
    f = open(K_SALIDA, "a", encoding="utf-8")

    bar = Bar('Generando listas de productos:', max=len(listas))
    f.write(K_INSERT)

    j=1
    i=0
    n_lista = 0

    for lista in listas:
        bar.next()
        
        n_lineas = random.randint(0, K_N_PRODUCTOS)
        n_lista+=1    
        linea = 0

        for _ in range(n_lineas):
            producto = productos[fake.unique.random_int(0,len(productos)-1)]       

            id_producto = str(producto[0])
            id_lista =  str(lista[0])

            f.write(K_VALUES.format(id_producto, id_lista))
        
            j+=1        
            i+=1
            linea+=1

            if j % K_DIV_INSERT == 0 or i == K_DIV_INSERT or (n_lista == len(listas) and linea == n_lineas):            
                f.write(';\n')
                if n_lista < len(listas):
                    f.write(K_INSERT)
            elif n_lista < len(listas) or linea < n_lineas:
                f.write(',\n')
        
        fake.unique.clear()

    bar.finish()		
    f.close();	

