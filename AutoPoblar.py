from generadores import gen_insert_categorias, gen_insert_chats_archivados, gen_insert_chats, gen_insert_clientes, gen_insert_direcciones, gen_insert_empleados, gen_insert_lineas_pedidos
from generadores import gen_insert_lista_producto, gen_insert_lista, gen_insert_mensajes_archivados, gen_insert_mensajes, gen_insert_pedido, gen_insert_productos, gen_insert_tarjetas
from generadores import gen_insert_transportes, gen_insert_usuarios, gen_insert_valoraciones, gen_insert_vendedores, generador_dni
import mysql.connector
import getpass
import os
from progress.bar import Bar
from timeit import default_timer as timer
from datetime import timedelta
from multiprocessing import Process
import winsound

DB_HOST = 'bbdd.dlsi.ua.es'
K_DELETE = "./static/delete.txt"

INSERTS1 = ["usuarios.sql", "categorias.sql", "clientes.sql", "direcciones.sql", "empleados.sql", "vendedores.sql",
           "productos.sql", "transportes.sql", "tarjetas.sql"]

INSERTS2 = ["listas.sql", "lineas_pedidos.sql", "chats.sql", "chats_archivados.sql", "valoraciones.sql"]

INSERTS3 = ["listas_producto.sql", "mensajes.sql", "mensajes_archivados.sql"]

def run_query(querys, db_user, db_name, db_pass):
    conn = mysql.connector.connect(host=DB_HOST, user=db_user, passwd=db_pass, database=db_name)
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8;")
    cursor.execute("SET CHARACTER SET utf8;")
    cursor.execute("SET character_set_connection=utf8;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

    bar = Bar('     Procesando', max=len(querys))

    for query in querys:
        #print(query)
        bar.next()
        if query not in ("", ";"):
            cursor.execute(query)
            cursor.execute("COMMIT;")

    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    cursor.execute("COMMIT;")
    bar.finish()
    cursor.close()
    conn.close()

def vaciatablas(db_user, db_name, db_pass):
    setter1 = "SET FOREIGN_KEY_CHECKS=0;"
    setter2 = "SET FOREIGN_KEY_CHECKS=1;"

    # fichero_deletes = open(K_DELETE)
    # deletes = fichero_deletes.readlines()
    # fdeletes = []

    # for delete in deletes:
    #     fdeletes.append(delete.format(db_name).replace("\n", ""))
    #     # run_query(setter1, db_user, db_name, db_pass)        
    #     # run_query(setter2, db_user, db_name, db_pass)

    with open(K_DELETE) as file:
        deletes = [line.strip().format(db_name) for line in file]

    print("+--------------------------+")
    print("| INICIO BORRADO DE TABLAS |")
    print("+--------------------------+")

    run_query(deletes, db_user, db_name, db_pass)

    print("+------------------------------+")
    print("| BORRADO DE TABLAS FINALIZADO |")
    print("+------------------------------+")


def insertar(db_user, db_name, db_pass, inserts):
    print("+--------------------------+")
    print("| INICIO INSERTS EN TABLAS |")
    print("+--------------------------+")

    for tabla in inserts:
        print('Insertando {}...'.format(tabla))
        sql_file = "./SQL/{}".format(tabla)

        # fd = open(ttabla, encoding="latin-1")
        # archivosql = fd.read()
        # sqlcommands = [elemento + ';' for elemento in archivosql.split(';')]
        # sqlcommands.pop()

        # run_query(sqlcommands, db_user, db_name, db_pass)

        with open(sql_file, encoding="latin-1") as file:
            sql_commands = file.read().split(';')[:-1]

        run_query(sql_commands, db_user, db_name, db_pass)

        # fd.close()
        
        

    print("+------------------------------+")
    print("| INSERTS EN TABLAS FINALIZADO |")
    print("+------------------------------+")

def main():
    db_user = input('Escribe tu usuario: ')
    db_name = input('Escribe tu database: ')
    db_pass = getpass.getpass('Contraseña: ')
    eliminar = input('¿Desea vaciar tablas? (S/n): ')
    generadores = input('¿Generar datasets? (s/N): ')
    nifs = input('¿Generar NIFs? (s/N): ')

    start = timer()

    if not(os.path.exists("./SQL") and os.path.isdir("./SQL")):
        os.mkdir("./SQL")

    if nifs in ["S", "s"]:
        generador_dni.main()

    if eliminar in ["S", "s", ""]:
        vaciatablas(db_user, db_name, db_pass)

    if generadores in ["S", "s"]:
        gen_insert_usuarios.main()
        gen_insert_categorias.main()
        gen_insert_clientes.main()
        gen_insert_direcciones.main()
        gen_insert_empleados.main()
        gen_insert_vendedores.main()
        gen_insert_productos.main()
        gen_insert_tarjetas.main()
        gen_insert_lista.main()
        gen_insert_chats_archivados.main()
        gen_insert_chats.main()
        gen_insert_transportes.main()
        gen_insert_valoraciones.main()

        insertar(db_user, db_name, db_pass, INSERTS1)

        gen_insert_pedido.main(db_user, db_name, db_pass)
        insertar(db_user, db_name, db_pass, ["pedidos.sql"])

        gen_insert_lineas_pedidos.main(db_user, db_name, db_pass)

        insertar(db_user, db_name, db_pass, INSERTS2)

        gen_insert_lista_producto.main(db_user, db_name, db_pass)
        gen_insert_mensajes_archivados.main(db_user, db_name, db_pass)
        gen_insert_mensajes.main(db_user, db_name, db_pass)

        insertar(db_user, db_name, db_pass, INSERTS3)
    else:
        insertar(db_user, db_name, db_pass, INSERTS1)
        insertar(db_user, db_name, db_pass, ["pedidos.sql"])
        insertar(db_user, db_name, db_pass, INSERTS2)
        insertar(db_user, db_name, db_pass, INSERTS3)

    end = timer()
    print("Tiempo de ejecución: {}".format(timedelta(seconds=end-start)))

    input("GENERACIÓN FINALIZADA CON ÉXITO. Pulsa enter para cerrar.")

if __name__ == "__main__":
	main()