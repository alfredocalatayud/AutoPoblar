import traceback

from faker import Faker
from progress.bar import Bar
from datetime import date
from os import remove, path
import random
import mysql.connector

DB_HOST = 'bbdd.dlsi.ua.es'

K_SALIDA = './SQL/pedidos.sql'
K_INSERT = 'insert pedido (id, total, fecha_pedido, coste_envio, tiempo_envio, nif_cliente, nif_transporte, id_dir_envio, id_dir_fact, num_tarjeta_bancaria) values '
K_VALUES = "({}, {}, '{}', {}, {}, AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)), '{}', {}, {}, AES_ENCRYPT('{}', SHA2('abcdefghijklmnopqrstuvwx', 512)))"
K_DIV_INSERT = 2000
K_N_PEDIDOS = 20
K_N_CHATS = 200

def run_query(query, conn):
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8;")
    cursor.execute("SET CHARACTER SET utf8;")
    cursor.execute("SET character_set_connection=utf8;")
    cursor.execute(query)

    salida = cursor.fetchall()

    cursor.close()
    conn.close()

    return salida 

def valor_cursor(cursor, clave):
    for dato in cursor:
        if clave == dato[0].decode('utf-8'):
            return dato[1]
        

def main(conn):
    fake = Faker('es_ES')

    if path.exists(K_SALIDA):
        remove(K_SALIDA)

    nif_clientes = run_query("SELECT AES_DECRYPT(nif, SHA2('abcdefghijklmnopqrstuvwx', 512)) FROM cliente;", conn)
    nif_transportes = run_query("SELECT nif FROM transporte;", conn)

    f = open(K_SALIDA, "x", encoding="utf-8")
    f = open(K_SALIDA, "a", encoding="utf-8")

    bar = Bar('Generando pedidos:', max=len(nif_clientes))
    f.write(K_INSERT)

    j = 1
    i = 0

    fecha_inicio = date(2021, 1, 1)
    fecha_fin = date(2023, 5, 1)
    n_nifs = 0


    for nif_cliente in nif_clientes:
        bar.next()
        n_nifs += 1

        nifcli = nif_cliente[0].decode('utf-8')
        # print(nifcli)

        try:
            num_tarjeta_bancarias = run_query("SELECT AES_DECRYPT(nif_cliente, SHA2('abcdefghijklmnopqrstuvwx', 512)) as nif_cliente, AES_DECRYPT(numero, SHA2('abcdefghijklmnopqrstuvwx', 512)) \
                                               FROM tarjeta_bancaria where nif_cliente = AES_ENCRYPT('" + nifcli + "', SHA2('abcdefghijklmnopqrstuvwx', 512));", conn)
        except Exception as e:
            print("Ocurrió el error: {}".format(e))
            traceback.print_exc()
            raise

        num_tarjeta_bancaria = valor_cursor(num_tarjeta_bancarias, nifcli)

        try:
            id_dir_envios = run_query("SELECT AES_DECRYPT(nif_usuario, SHA2('abcdefghijklmnopqrstuvwx', 512)) as nif_usuario, id FROM direccion where nif_usuario = AES_ENCRYPT('" + nifcli + "', SHA2('abcdefghijklmnopqrstuvwx', 512));", conn)
        except Exception as e:
            print("Ocurrió el error: {}".format(e))
            traceback.print_exc()
            raise

        id_dir_envio = valor_cursor(id_dir_envios, nifcli)
        id_dir_fact = id_dir_envio
        
        n_pedidos = random.randint(0, K_N_PEDIDOS)
        n_pedido = 0
            
        for _ in range(n_pedidos):
            id = str(j)
            total = 0
            fecha_pedido = fake.date_between(fecha_inicio, fecha_fin)        
            coste_envio = round(random.uniform(1.00, 10.00), 2)
            tiempo_envio = random.randint(1, 30)
            i_nif_cliente = nifcli
            nif_transporte = nif_transportes[random.randint(0, len(nif_transportes)-1)]
            
            # print(K_VALUES.format(id, str(total), str(fecha_pedido), str(coste_envio), str(tiempo_envio), i_nif_cliente, nif_transporte[0], str(id_dir_envio), str(id_dir_fact), num_tarjeta_bancaria.decode('utf-8')))
            f.write(K_VALUES.format(id, str(total), str(fecha_pedido), str(coste_envio), str(tiempo_envio), i_nif_cliente, nif_transporte[0], str(id_dir_envio), str(id_dir_fact), num_tarjeta_bancaria.decode('utf-8')))
        
            j += 1
            i += 1
            n_pedido += 1
            
            if i % K_DIV_INSERT == 0 or i == K_DIV_INSERT or (n_nifs == len(nif_clientes) and n_pedido == n_pedidos):
                f.write(';\n')
                if n_nifs < len(nif_clientes):
                    f.write(K_INSERT)
            elif n_nifs < len(nif_clientes) or n_pedido < n_pedidos:
                f.write(',\n')
        
        fake.unique.clear()

    bar.finish()		
    f.close();	

if __name__ == "__main__":
    main()