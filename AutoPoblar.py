import sys
import platform
import time
import mysql.connector
import getpass
import os
from progress.bar import Bar
from timeit import default_timer as timer
from datetime import timedelta

from generadores import gen_insert_categorias, gen_insert_chats_archivados, gen_insert_chats, gen_insert_clientes, gen_insert_direcciones, gen_insert_empleados, gen_insert_lineas_pedidos
from generadores import gen_insert_lista_producto, gen_insert_lista, gen_insert_mensajes_archivados, gen_insert_mensajes, gen_insert_pedido, gen_insert_productos, gen_insert_tarjetas
from generadores import gen_insert_transportes, gen_insert_usuarios, gen_insert_valoraciones, gen_insert_vendedores, generador_dni
from utiles import informacion as info

if sys.platform.startswith('win'):
    LIMPIAR = "cls"
else:
    LIMPIAR = "clear" 

DB_HOST = 'bbdd.dlsi.ua.es'
K_DELETE = "./static/delete.txt"

INSERTS1 = ["usuarios.sql", "categorias.sql", "clientes.sql", "direcciones.sql", "empleados.sql", "vendedores.sql",
           "productos.sql", "transportes.sql", "tarjetas.sql"]

INSERTS2 = ["listas.sql", "lineas_pedidos.sql", "chats.sql", "chats_archivados.sql", "valoraciones.sql"]

INSERTS3 = ["listas_producto.sql", "mensajes.sql", "mensajes_archivados.sql"]

TITULO = """888b. w                                w    8                     db           w         888b.       8    8           
8wwwP w .d88b 8d8b. Yb  dP .d88b 8d8b. w .d88 .d8b.    .d88      dPYb   8   8 w8ww .d8b. 8  .8 .d8b. 88b. 8 .d88 8d8b 
8   b 8 8.dP' 8P Y8  YbdP  8.dP' 8P Y8 8 8  8 8' .8    8  8     dPwwYb  8b d8  8   8' .8 8wwP' 8' .8 8  8 8 8  8 8P   
888P' 8 `Y88P 8   8   YP   `Y88P 8   8 8 `Y88 `Y8P'    `Y88    dP    Yb `Y8P8  Y8P `Y8P' 8     `Y8P' 88P' 8 `Y88 8\n"""

def run_query(querys, conn):
    cursor = conn.cursor()
    # cursor.execute("SET NAMES utf8;")
    # cursor.execute("SET     CHARACTER SET utf8;")
    # cursor.execute("character set=latin1;")
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

    bar = Bar('     Procesando', max=len(querys))

    for query in querys:
        #print(query)
        bar.next()
        if query not in ("", ";"):
            cursor.execute(query + ");")
            cursor.execute("COMMIT;")

    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    cursor.execute("COMMIT;")
    bar.finish()

def vaciatablas(conn):
    setter1 = "SET FOREIGN_KEY_CHECKS=0;"
    setter2 = "SET FOREIGN_KEY_CHECKS=1;"

    with open(K_DELETE) as file:
        deletes = [line.strip().format(conn.database) for line in file]

    print("+--------------------------+")
    print("| INICIO BORRADO DE TABLAS |")
    print("+--------------------------+")

    run_query(deletes, conn)

    print("+------------------------------+")
    print("| BORRADO DE TABLAS FINALIZADO |")
    print("+------------------------------+")

def newVaciaTablas(conn = mysql.connector.connect()):
    cursor = conn.cursor()

    with open(K_DELETE) as file:
        deletes = [line.strip() for line in file]
    
    print("+--------------------------+")
    print("| INICIO BORRADO DE TABLAS |")
    print("+--------------------------+")

    bar = Bar('     Procesando', max=len(deletes))
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")

    for delete in deletes:
        t_lote = 50000

        while True:
            
            cursor.execute(delete.format(conn.database, t_lote))
            filas_modificadas = cursor.rowcount

            if filas_modificadas == 0:
                break
        bar.next()
    bar.finish()

    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
    cursor.execute("commit;")

    print("+------------------------------+")
    print("| BORRADO DE TABLAS FINALIZADO |")
    print("+------------------------------+")

def insertar(conn, inserts):
    print("+--------------------------+")
    print("| INICIO INSERTS EN TABLAS |")
    print("+--------------------------+")

    for tabla in inserts:
        print('Insertando {}...'.format(tabla))
        sql_file = "./SQL/{}".format(tabla)

        with open(sql_file, encoding="latin-1") as file:
            # sql_commands = file.read().split(';')[:-1]
            sql_commands = file.read().split(');')[:-1]

        run_query(sql_commands, conn)

    print("+------------------------------+")
    print("| INSERTS EN TABLAS FINALIZADO |")
    print("+------------------------------+")

def insertaFichero(conn, ficheros):
    for fichero in ficheros:
        ejectutaFichero(conn, "./SQL/{}".format(fichero), "Insertando {}".format(fichero))

def ejectutaFichero(conn, fichero, mensaje):
    conn.reconnect()
    print(mensaje)
    cursor = conn.cursor()
    with open(fichero, 'r') as myfile:
        data = myfile.read()
        # cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.execute(data, multi=True)
        # cursor.execute("SET FOREIGN_KEY_CHECKS=1;")


def datasetsPlusInserta(conn):
    print("+------------------------------+")
    print("|      GENERANDO DATASETS      |")
    print("+------------------------------+")

    generador_dni.main()
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
    
    insertar(conn, INSERTS1)

    gen_insert_pedido.insertar(conn)
    insertar(conn, ["pedidos.sql"])

    gen_insert_lineas_pedidos.main(conn)

    insertar(conn, INSERTS2)

    gen_insert_lista_producto.main(conn)
    gen_insert_mensajes_archivados.main(conn)
    gen_insert_mensajes.main(conn)

    insertar(conn, INSERTS3)

def insertaTodo(conn):
    insertar(conn, INSERTS1)
    insertar(conn, ["pedidos.sql"])
    insertar(conn, INSERTS2)
    insertar(conn, INSERTS3)

def numTablas(conn):
    conn.reconnect()
    cursor = conn.cursor()

    cursor.execute("select count(*) as tables from information_schema.tables where table_type = 'BASE TABLE' and table_schema not in ('information_schema', 'sys', 'performance_schema', 'mysql') and TABLE_SCHEMA = '{}' group by table_schema order by table_schema;".format(conn.database))

    salida = cursor.fetchall()

    try:
        return(salida[0][0])
    except IndexError:
        return 0

def pruebaConexion(db_user, db_name, db_pass):
    try:
        sesion = mysql.connector.connect(host=DB_HOST, user=db_user, passwd=db_pass, database=db_name)
        return sesion
    except mysql.connector.errors.InterfaceError  as interno:
        print("\n")
        if interno.errno == 1044:
            input("Error: Base de datos no accesible. Vuelve a intentarlo...")    
        elif interno.errno == 1045:
            input("Error: Usuario o contraseña incorrectos. Vuelve a intentarlo...")
        elif interno.errno == 2003:
            input("Error: Comprueba el estado del puerto. Vuelve a intentarlo...")
        else:
            print(interno)
    except mysql.connector.errors.DatabaseError  as e:
        print("\n")
        if e.errno == 1044:
            input("Error: Base de datos no accesible. Vuelve a intentarlo...")    
        elif e.errno == 1045:
            input("Error: Usuario o contraseña incorrectos. Vuelve a intentarlo...")
        elif e.errno == 2003:
            input("Error: Comprueba el estado del puerto. Vuelve a intentarlo...")
        else:
            print(e)
    
    os.system(LIMPIAR)
    return False

def generacionCompleta(conn):
    os.system(LIMPIAR)
    print(TITULO)

    if not(os.path.exists("./SQL") and os.path.isdir("./SQL")):
        os.mkdir("./SQL")

    start = timer()

    print("+--------------------------+")
    print("|    INICIANDO CREACIÓN    |")
    print("+--------------------------+")

    ejectutaFichero(conn, "./static/drop_triggers.sql", "¡Borrando triggers!")
    ejectutaFichero(conn, "./static/drop_functions.sql", "¡Borrando funciones!")
    ejectutaFichero(conn, "./static/drop_procedures.sql", "¡Borrando procesos!")
    ejectutaFichero(conn, "./static/drop_events.sql", "¡Borrando eventos!")
    ejectutaFichero(conn, "./static/drop_views.sql", "¡Borrando vistas!")
    ejectutaFichero(conn, "./static/drop_tables.sql", "¡Borrando tablas!")
    try:
        ejectutaFichero(conn, "./static/drop_indices.sql", "¡Borrando indices!")   
    except:
        print("No es necesario borrar índices")
        pass
    
    ejectutaFichero(conn, "./static/create_tables.sql", "¡Creando tablas!")
    time.sleep(15)
    tablas = numTablas(conn)

    while(tablas < 18):
        ejectutaFichero(conn, "./static/create_tables.sql", "Creación de tablas en progreso...")
        time.sleep(15)
        tablas = numTablas(conn)

    ejectutaFichero(conn, "./static/create_triggers1.sql", "¡Primeros triggers creados!")   
    conn.reconnect()
    datasetsPlusInserta(conn)
    #insertaTodo(db_user, db_name, db_pass)

    ejectutaFichero(conn, "./static/create_triggers2.sql", "¡Resto de triggers creados!")
    ejectutaFichero(conn, "./static/create_functions.sql", "¡Funciones creadas!")
    ejectutaFichero(conn, "./static/create_procedures.sql", "¡Procesos creados!")
    ejectutaFichero(conn, "./static/create_views.sql", "¡Vistas creadas!")
    ejectutaFichero(conn, "./static/create_events.sql", "¡Eventos creados!")
    ejectutaFichero(conn, "./static/create_indices.sql", "¡Índices creados!")

    print("+--------------------------+")
    print("|       FIN  CREACIÓN      |")
    print("+--------------------------+")
    
    end = timer()

    print("Tiempo de ejecución: {}".format(timedelta(seconds=end-start)))
    input("GENERACIÓN FINALIZADA CON ÉXITO. Pulsa enter para cerrar.")
    os.system(LIMPIAR)

def insertaDatasets(conn):
    # insertar(db_user, db_name, db_pass, INSERTS1)
    # insertar(db_user, db_name, db_pass, ["pedidos.sql"])
    # insertar(db_user, db_name, db_pass, INSERTS2)
    # insertar(db_user, db_name, db_pass, INSERTS3)

    insertar(conn, INSERTS1 + ["pedidos.sql"] + INSERTS2 + INSERTS3)

    # insertaFichero(db_user, db_name, db_pass, INSERTS1)
    # insertaFichero(db_user, db_name, db_pass, ["pedidos.sql"])
    # insertaFichero(db_user, db_name, db_pass, INSERTS2)
    # insertaFichero(db_user, db_name, db_pass, INSERTS3)

def informacionBBDD(conn):
    conn.reconnect()
    option = ""
    while option != "X":
        os.system(LIMPIAR)
        print(TITULO)

        print("+--------------------+")
        print("|  Información BBDD  |")
        print("+--------------------+\n")

        print(" [0] Tablas.")
        print(" [1] Vistas.")
        print(" [2] Triggers.")
        print(" [3] Funciones.")
        print(" [4] Procesos.")
        print(" [5] Eventos.")
        print(" [6] Vendedor.")
        print(" [7] Cliente.")
        print(" [8] Empleado.")
        print(" [X] Salir.")

        option = input("\nElige tu opción: ")

        if option in ["X", "x"]:
            return 0

        if option == "0":
            info.informacionTabla(conn)
        elif option == "1":
            info.informacionVistas(conn)
        elif option == "2":
            info.informacionTriggers(conn)
        elif option == "3":
            info.informacionFuncion(conn)
        elif option == "4":
            info.informacionProcesos(conn)
        elif option == "5":
            info.informacionEventos(conn)
        elif option == "6":
            info.getVendedor(conn)
        elif option == "7":
            info.getCliente(conn)
        elif option == "8":
            info.getEmpleado(conn)
        else:
            input("\nOpción no válida...")


def inicioSesion():
    while True:
        os.system(LIMPIAR)
        print(TITULO)
        db_user = input('Escribe tu usuario: ')
        db_name = input('Escribe tu database: ')
        db_pass = getpass.getpass('Contraseña: ')

        sesion = pruebaConexion(db_user, db_name, db_pass)

        if sesion:
            os.environ["db_user"] = db_user
            os.environ["db_name"] = db_name
            os.environ["db_pass"] = db_pass
            input("\n¡Sesión iniciada correctamente! Pulsa enter para volver al menú...")
            return sesion

def menu():
    sesion = False
    option = ""
    while option != "X":
        os.system(LIMPIAR)
        print(TITULO)

        print("+--------+")
        print("|  Menú  |")
        print("+--------+\n")
        print(" [0] Iniciar sesión.")
        print(" [1] Crear base de datos desde cero.")
        print(" [2] Crear datasets nuevos.")
        print(" [3] Vaciar base de datos.")
        print(" [4] Insertar datasets existentes.")
        print(" [5] Ver información BBDD")
        print(" [X] Salir.")

        option = input("\nElige tu opción: ")

        if option in  ["X", "x"]:
            break

        if option == "0":
            conn = inicioSesion()
            sesion = True
        elif (not sesion):
            input("\nEs necesario iniciar sesión primero...")
        else:
            if option == "1":
                continuar = input("\nEsta opción eliminará cualquier información existente en la BBDD. ¿Desea continuar? (S/n): ")
                if continuar in ["S", "s", ""]:
                    generacionCompleta(conn)
            elif option == "2":
                pass
            elif option == "3":
                continuar = input("\nEsta opción eliminará los datos de la BBDD. ¿Desea continuar? (S/n): ")
                if continuar in ["S", "s", ""]:
                    os.system(LIMPIAR)
                    print(TITULO)
                    newVaciaTablas(conn)
                    input("\n¡Información borrada con éxito! Pulsa enter para volver al menú...")
            elif option == "4":
                continuar = input("\nRecuerda, antes de realizar este paso has de lanzar [3]. ¿Desea continuar? (S/n): ")
                if continuar in ["S", "s", ""]:
                    insertaDatasets(conn)
                    input("\n¡Información insertada con éxito! Pulsa enter para volver al menú...")
                    
            elif option == "5":
                informacionBBDD(conn)
            else:
                input("\nOpción no válida...")
    
    os.system(LIMPIAR)


def main():
    menu()

if __name__ == "__main__":
	main()