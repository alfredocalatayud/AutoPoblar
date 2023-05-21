from faker import Faker
from progress.bar import Bar
from datetime import date, time, datetime
from os import remove, path
import secrets, string, random, os, time
#from mysql import connector 
import mysql.connector

DB_HOST = 'bbdd.dlsi.ua.es'
DB_USER = 'gi_acs128'
DB_PASS = 'Caramelos1998'
DB_NAME = 'gi_tierra_alicante'

def run_query(query=''):
    datos =  [DB_HOST, DB_USER, DB_PASS, DB_NAME]
    
    conn = mysql.connector.connect(host = DB_HOST, user = DB_USER, passwd = DB_PASS, database = DB_NAME)
    conn.set_character_set_name('utf8')
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8;")
    cursor.execute("SET CHARACTER SET utf8;")
    cursor.execute("SET character_set_connection=utf8;")
    cursor.execute(query)

    print(conn)

    salida = cursor.fetchall()

    cursor.close()
    conn.close()

    return salida 
    
fake = Faker('es_ES')

K_SALIDA = 'listas_producto.sql'
K_NIFS = "nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert producto_lista (id_producto, id_lista) values '
K_DIV_INSERT = 2000
K_N_PRODUCTOS = 30
K_N_CHATS = 200

if path.exists(K_SALIDA):
    remove(K_SALIDA)
    
productos = run_query('SELECT id FROM producto order by id asc;')
listas = run_query('SELECT id FROM lista order by id asc;')

f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

bar = Bar('Generando listas:', max=len(listas))
f.write(K_INSERT)

j=1
i=0

for lista in listas:
    bar.next()
        
    for _ in range(random.randint(0, K_N_PRODUCTOS)):
        producto = productos[fake.unique.random_int(0,len(productos)-1)]        
        
        f.write('(\'' + str(producto[0]) + '\', \'' + str(lista[0]) + '\')')
    
        j+=1        
        i+=1
        
        if i % K_DIV_INSERT == 0:
            f.write(';\n')
            f.write(K_INSERT)
        else:
            f.write(',\n')
    
    fake.unique.clear()

bar.finish()		
f.close();	

