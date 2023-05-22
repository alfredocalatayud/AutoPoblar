import re
from progress.bar import Bar
import os
import mysql.connector
import getpass

DB_HOST = 'bbdd.dlsi.ua.es'
K_DELETE = "delete.txt"

INSERTS = ["usuarios.sql", "categorias.sql", "clientes.sql", "direcciones.sql", "empleados.sql", "vendedores.sql",
           "productos.sql", "transportes.sql", "tarjetas.sql", "pedidos.sql", \
           "lineas_pedidos.sql", "listas.sql", "listas_producto.sql", "chats.sql", "chats_archivados.sql",
           "mensajes.sql", "mensajes_archivados.sql", "valoraciones.sql"]


def run_query(querys, db_user, db_name, db_pass):
    conn = mysql.connector.connect(host=DB_HOST, user=db_user, passwd=db_pass, database=db_name)
    # conn.set_character_set_name('utf8')
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8;")
    cursor.execute("SET CHARACTER SET utf8;")
    cursor.execute("SET character_set_connection=utf8;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

    bar = Bar('Procesando', max=len(querys))

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

    return 0


def vaciatablas(db_user, db_name, db_pass):
    setter1 = "SET FOREIGN_KEY_CHECKS=0;"
    setter2 = "SET FOREIGN_KEY_CHECKS=1;"

    fichero_deletes = open(K_DELETE)
    deletes = fichero_deletes.readlines()
    fdeletes = []

    print("| -------------------------|")
    print("| INICIO BORRADO DE TABLAS |")
    print("| -------------------------|")

    for delete in deletes:
        fdeletes.append(delete.format(db_name).replace("\n", ""))
        # run_query(setter1, db_user, db_name, db_pass)        
        # run_query(setter2, db_user, db_name, db_pass)

    run_query(fdeletes, db_user, db_name, db_pass)

    print("| -----------------------------|")
    print("| BORRADO DE TABLAS FINALIZADO |")
    print("| -----------------------------|")


def insertar(db_user, db_name, db_pass):
    print("| -------------------------|")
    print("| INICIO INSERTS EN TABLAS |")
    print("| -------------------------|")

    for tabla in INSERTS:
        print('Insertando ' + tabla + '...')
        # comando = 'mysql -h ' + DB_HOST + ' -u ' + db_user + ' -p\'' + db_pass + '\' ' + db_name + ' < ' + tabla + ' > /dev/null'
        # os.system(comando)

        fd = open(tabla, encoding="utf8")
        archivosql = fd.read()
        # sqlcommands = re.split(';', archivosql)
        sqlcommands = [elemento + ';' for elemento in archivosql.split(';')]
        sqlcommands.pop()

        run_query(sqlcommands, db_user, db_name, db_pass)

        fd.close()
        # for command in sqlcommands:

    print("| -----------------------------|")
    print("| INSERTS EN TABLAS FINALIZADO |")
    print("| -----------------------------|")


db_user = input('Escribe tu usuario: ')
db_name = input('Escribe tu database: ')
db_pass = getpass.getpass('Contraseña: ')
eliminar = input('¿Desea vaciar tablas (S/n)?: ')

if eliminar in ["S", "s", ""]:
    vaciatablas(db_user, db_name, db_pass)

insertar(db_user, db_name, db_pass)
