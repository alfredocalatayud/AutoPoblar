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

K_SALIDA = 'lineas_pedidos.sql'
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into linea_pedido (id, cantidad, precio, base, iva, subtotal, estado, fecha_envio, fecha_recepcion, id_producto, id_pedido, nif_vendedor) values '
K_DIV_INSERT = 2000
K_N_PEDIDOS = 2000
K_N_PRODUCTOS = 30
K_ESTADOS = ["Pendiente", "Confirmado", "Enviado", "Entregado", "Cancelado", "Devuelto", "Rechazado"]

if path.exists(K_SALIDA):
    remove(K_SALIDA)

productos = run_query('SELECT id, precio, iva, nif_vendedor FROM producto;')
fechas_pedido = run_query('SELECT fecha_pedido from pedido;')
nif_transportes = run_query('SELECT nif FROM transporte;')

f = open(K_SALIDA, "x")
f = open(K_SALIDA, "a")

bar = Bar('Generando pedidos:', max = K_N_PEDIDOS)
f.write(K_INSERT)

j=0
i=0

fecha_inicio = date(2021, 1, 1)
fecha_fin = date(2023, 5, 1)

for i in range(0, K_N_PEDIDOS):
    bar.next()

    id_pedido = i+1
        
    for _ in range(0, random.randint(0, K_N_PRODUCTOS)):
        fecha_envio = 'NULL'
        fecha_recepcion = 'NULL'
        
        if fake.boolean(chance_of_getting_true=75):
            fecha_envio = fake.date_between(fecha_inicio, fecha_fin)
            fecha_pedido = fechas_pedido[i][0]
            while fecha_pedido.date() > fecha_envio:   
                fecha_envio = fake.date_between(fecha_inicio, fecha_fin)
        
        if fecha_envio != 'NULL' and fake.boolean(chance_of_getting_true=60):
            fecha_recepcion = fake.date_between(fecha_inicio, fecha_fin)
            while fecha_envio > fecha_recepcion:   
                fecha_recepcion = fake.date_between(fecha_inicio, fecha_fin)

        producto = productos[fake.unique.random_int(min = 0, max = len(productos)-1)]
        cantidad = random.randint(1, 200)
        precio = producto[1]
        base = cantidad * precio
        iva = producto[2]
        subtotal = round(precio * (1+iva), 2)
        estado = K_ESTADOS[random.randint(0,6)]
        f_envio = "'" + str(fecha_envio) + "'" if fecha_envio != 'NULL' else 'NULL'
        f_recepcion = "'" + str(fecha_recepcion) + "'" if fecha_recepcion != 'NULL' else 'NULL'
        id_producto = producto[0]
        nif_vendedor = producto[3]

        f.write('(' + str(j) + ', ' + str(cantidad) + ', ' + str(precio) + ', ' + str(base) + ', ' + str(iva) + ', ' + str(subtotal) + ', \'' + estado + '\', ' \
                    + f_envio + ', ' + f_recepcion + ', ' + str(id_producto) + ', ' + str(id_pedido) + ', \'' + nif_vendedor + '\')')
    
        j+=1     
        
        if j % K_DIV_INSERT == 0:
            f.write(';\n')
            f.write(K_INSERT)
        else:
            f.write(',\n')
    
    fake.unique.clear()

bar.finish()		
f.close();	

