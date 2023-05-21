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

    #print(conn)

    salida = cursor.fetchall()

    cursor.close()
    conn.close()

    return salida 

def valor_cursor(cursor, clave):
    for dato in cursor:
        if clave == dato[0]:
            return dato[1]
        

fake = Faker('es_ES')

K_SALIDA = 'pedidos.sql'
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert pedido (id, total, fecha_pedido, coste_envio, tiempo_envio, nif_cliente, nif_transporte, id_dir_envio, id_dir_fact, num_tarjeta_bancaria) values '
K_DIV_INSERT = 2000
K_N_PEDIDOS = 20
K_N_CHATS = 200

if path.exists(K_SALIDA):
    remove(K_SALIDA)

nif_clientes = run_query('SELECT nif FROM cliente;')
nif_transportes = run_query('SELECT nif FROM transporte;')

f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

bar = Bar('Generando pedidos:', max=len(nif_clientes))
f.write(K_INSERT)

j=1
i=0

fecha_inicio = date(2021, 1, 1)
fecha_fin = date(2023, 5, 1)


for nif_cliente in nif_clientes:
    bar.next()

    num_tarjeta_bancarias = run_query('SELECT nif_cliente, numero FROM tarjeta_bancaria where nif_cliente = \'' + nif_cliente[0] + '\';')
    num_tarjeta_bancaria = valor_cursor(num_tarjeta_bancarias, nif_cliente[0])

    id_dir_envios = run_query('SELECT nif_usuario, id FROM direccion where nif_usuario = \'' + nif_cliente[0] + '\';')
    id_dir_envio = valor_cursor(id_dir_envios, nif_cliente[0])
    id_dir_fact = id_dir_envio
    
        
    for _ in range(random.randint(0, K_N_PEDIDOS)):
        total = 0
        fecha_pedido = fake.date_between(fecha_inicio, fecha_fin)
        
        
        coste_envio = round(random.uniform(1.00, 10.00), 2)
        tiempo_envio = random.randint(0, 60)
        nif_transporte = nif_transportes[random.randint(0, len(nif_transportes)-1)]
        
        
        f.write('(' + str(j) + ', ' + str(total) + ', \'' + str(fecha_pedido) + '\', ' + str(coste_envio) + ', ' + str(tiempo_envio) + ', \'' \
                    + nif_cliente[0] + '\', \'' + nif_transporte[0] + '\', ' + str(id_dir_envio) + ', ' + str(id_dir_fact) + ', \'' + num_tarjeta_bancaria  + '\')')
    
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

