import datetime
from faker import Faker
from progress.bar import Bar
import datetime
from datetime import date
from datetime import datetime
from os import remove, path
import random
import mysql.connector

DB_HOST = 'bbdd.dlsi.ua.es'

K_SALIDA = './SQL/lineas_pedidos.sql'
K_LETRAS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
K_INSERT = 'insert into linea_pedido (id, cantidad, precio, base, iva, subtotal, estado, fecha_envio, fecha_recepcion, id_producto, id_pedido) values '
K_VALUES = "({}, {}, {}, {}, {}, {}, '{}', {}, {}, '{}', {})"
K_DIV_INSERT = 2000
K_N_PEDIDOS = 2000
K_N_PRODUCTOS = 30
K_ESTADOS = ["Cesta", "Pendiente", "Confirmado", "Enviado", "Entregado", "Cancelado", "Devuelto", "Rechazado", "En devolucion"]

def run_query(query, conn):
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8;")
    cursor.execute("SET CHARACTER SET utf8;")
    cursor.execute("SET character_set_connection=utf8;")
    cursor.execute(query)

    salida = cursor.fetchall()

    cursor.close()

    return salida 

def valor_cursor(cursor, clave):
    for dato in cursor:
        if clave == dato[0]:
            return dato[1]
        

fake = Faker('es_ES')

def main(conn): 
    if path.exists(K_SALIDA):
        remove(K_SALIDA)

    productos = run_query("SELECT id, precio, iva, AES_DECRYPT(nif_vendedor, SHA2('abcdefghijklmnopqrstuvwx', 512)) FROM producto;", conn)
    pedidos = run_query("SELECT AES_DECRYPT(nif_cliente, SHA2('abcdefghijklmnopqrstuvwx', 512)), date_format(fecha_pedido, '%Y/%m/%d') from pedido;", conn)

    K_N_PEDIDOS = len(pedidos)

    f = open(K_SALIDA, "x", encoding="utf-8")
    f = open(K_SALIDA, "a", encoding="utf-8")

    bar = Bar('Generando lineas de pedidos:', max = K_N_PEDIDOS)
    f.write(K_INSERT)

    j = 0
    i = 0

    fecha_inicio = date(2021, 1, 1)
    fecha_fin = date(2023, 5, 1)

    estados = K_ESTADOS
    tiene_cesta = False

    for i in range(0, K_N_PEDIDOS):
        bar.next()

        id_pedido = i+1

        n_lineas = random.randint(0, K_N_PRODUCTOS)
        linea = 0

        if i == 0:
            cliente = pedidos[i][0]

        cliente_actual = pedidos[i][0]

        if cliente != cliente_actual:
            tiene_cesta = False
            cliente = cliente_actual
            
        for _ in range(0, n_lineas):
            fecha_envio = 'NULL'
            fecha_recepcion = 'NULL'

            if tiene_cesta:
                estado = estados[random.randint(1,len(estados)-1)]
            else:
                estado = estados[random.randint(0,len(estados)-1)]

            if estado == "Cesta":
                tiene_cesta = True

            if estado in ("Enviado", "Entregado", "Devuelto", "Rechazado", "En devolucion", "Cancelado"):
                fecha_envio = fake.date_between(fecha_inicio, fecha_fin)
                fecha_pedido = datetime.strptime(pedidos[i][1], "%Y/%m/%d")
                while fecha_pedido.date() > fecha_envio:   
                    fecha_envio = fake.date_between(fecha_inicio, fecha_fin)
            
            if fecha_envio != 'NULL' and estado in ("Entregado", "Devuelto", "En devolucion"):
                fecha_recepcion = fake.date_between(fecha_inicio, fecha_fin)
                while fecha_envio > fecha_recepcion:   
                    fecha_recepcion = fake.date_between(fecha_inicio, fecha_fin)
            
            id = str(j)
            producto = productos[fake.unique.random_int(min = 0, max = len(productos)-1)]
            cantidad = random.randint(1, 200)
            precio = producto[1]
            iva = producto[2]
            base = round(precio / (1+iva), 2) * cantidad
            subtotal = cantidad * precio
            f_envio = "'" + str(fecha_envio) + "'" if fecha_envio != 'NULL' else 'NULL'
            f_recepcion = "'" + str(fecha_recepcion) + "'" if fecha_recepcion != 'NULL' else 'NULL'
            id_producto = producto[0]

            f.write(K_VALUES.format(id, str(cantidad), str(precio), str(base), str(iva), str(subtotal), estado, f_envio, f_recepcion, id_producto, str(id_pedido)))
            
            j+=1  
            linea+=1   
            
            if j % K_DIV_INSERT == 0 or i == K_DIV_INSERT or (i == K_N_PEDIDOS-1 and linea == n_lineas):
                f.write(';\n')
                if i < K_N_PEDIDOS-1:
                    f.write(K_INSERT)
            elif i < K_N_PEDIDOS:
                f.write(',\n')
        
        fake.unique.clear()

    bar.finish()		
    f.close()


if __name__ == "__main__":
    main()
