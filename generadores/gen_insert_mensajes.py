from faker import Faker
from progress.bar import Bar
from datetime import date, time, datetime
from os import remove, path
import random
import mysql.connector

DB_HOST = 'bbdd.dlsi.ua.es'

K_SALIDA = './SQL/mensajes.sql'
K_NIFS = "./static/nifs.txt"
K_INSERT = 'insert into mensaje (id, id_chat, nif_usuario, fecha_envio, contenido) values '
K_VALUES = "({}, {}, '{}', '{}', AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)))"
K_DIV_INSERT = 2000
K_N_MENSAJES = 10
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
        
    chats = run_query('SELECT * FROM chat', db_user, db_name, db_pass)

    f = open(K_SALIDA, "x", encoding="utf-8")
    f = open(K_SALIDA, "a", encoding="utf-8")

    fichero_nifs = open(K_NIFS, encoding="utf-8")
    nifs = fichero_nifs.readlines()

    bar = Bar('Generando mensajes:', max=K_N_CHATS)
    f.write(K_INSERT)

    j=1
    i=0
    n_chat = 0

    for chat in chats:
        bar.next()
        fecha_inicio = chat[3]
        fecha_fin = chat[4]
        id_chat = chat[0]
        n_chat+=1

        n_mensajes = random.randint(K_N_MENSAJES, K_N_MENSAJES*2)
        mensaje = 0 
        
        for k in range(n_mensajes):

            id = str(j)
            id_chat = str(id_chat)
            nif_usuario = chat[random.randint(1,2)]
            fecha_envio = str(fake.date_between(fecha_inicio, fecha_fin))
            contenido = fake.text(max_nb_chars=200)        
            
            # f.write('(' + str(j) + ', ' + str(id_chat) + ', \'' + nif_usuario + '\', \'' + str(fecha_envio) + '\', \'' + contenido + '\')')
            f.write(K_VALUES.format(id, id_chat, nif_usuario, fecha_envio, contenido))
        
            j+=1        
            i+=1
            mensaje+=1
            
            if i % K_DIV_INSERT == 0 or i == K_DIV_INSERT or (n_chat == len(chats) and mensaje == n_mensajes):
                f.write(';\n')
                if n_chat < len(chats):
                    f.write(K_INSERT)
            elif n_chat < len(chats) or mensaje < n_mensajes:
                f.write(',\n')
        
    bar.finish()		
    f.close();	

