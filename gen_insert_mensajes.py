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

K_SALIDA = 'mensajes_archivados.sql'
K_NIFS = "nifs.txt"
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into mensaje_archivado (id, id_chat, nif_usuario, fecha_envio, contenido) values '
K_DIV_INSERT = 2000
K_N_MENSAJES = 10
K_N_CHATS = 200

if path.exists(K_SALIDA):
    remove(K_SALIDA)
    
chats = run_query('SELECT * FROM chat')

f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

fichero_nifs = open(K_NIFS)
nifs = fichero_nifs.readlines()

bar = Bar('Generando mensajes:', max=K_N_CHATS)
f.write(K_INSERT)

j=1
i=0

for chat in chats:
    bar.next()
    fecha_inicio = chat[3]
    fecha_fin = chat[4]
    id_chat = chat[0]
    
    for k in range(random.randint(K_N_MENSAJES, K_N_MENSAJES*2)):
        nif_usuario = chat[random.randint(1,2)]
        fecha_envio = fake.date_between(fecha_inicio, fecha_fin)
        contenido = fake.text(max_nb_chars=200)
        
        
        f.write('(' + str(j) + ', ' + str(id_chat) + ', \'' + nif_usuario + '\', \'' + str(fecha_envio) + '\', \'' + contenido + '\')')
    
        j+=1        
        i+=1
        
        if i % K_DIV_INSERT == 0:
            f.write(';\n')
            f.write(K_INSERT)
        else:
            f.write(',\n')
    
bar.finish()		
f.close();	

