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

        with open(sql_file, encoding="latin-1") as file:
            sql_commands = file.read().split(';')[:-1]

        run_query(sql_commands, db_user, db_name, db_pass)

    print("+------------------------------+")
    print("| INSERTS EN TABLAS FINALIZADO |")
    print("+------------------------------+")

def insertaFichero(db_user, db_name, db_pass, ficheros):
    for fichero in ficheros:
        ejectutaFichero(db_user, db_name, db_pass, "./SQL/{}".format(fichero), "Insertando {}".format(fichero))

def ejectutaFichero(db_user, db_name, db_pass, fichero, mensaje):
    print(mensaje)
    with open(fichero, 'r') as myfile:
        conn = mysql.connector.connect(host=DB_HOST, user=db_user, passwd=db_pass, database=db_name)
        cursor = conn.cursor()
        data = myfile.read()
        cursor.execute(data)


def datasetsPlusInserta(db_user, db_name, db_pass):
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
    
    insertar(db_user, db_name, db_pass, INSERTS1)

    gen_insert_pedido.main(db_user, db_name, db_pass)
    insertar(db_user, db_name, db_pass, ["pedidos.sql"])

    gen_insert_lineas_pedidos.main(db_user, db_name, db_pass)

    insertar(db_user, db_name, db_pass, INSERTS2)

    gen_insert_lista_producto.main(db_user, db_name, db_pass)
    gen_insert_mensajes_archivados.main(db_user, db_name, db_pass)
    gen_insert_mensajes.main(db_user, db_name, db_pass)

    insertar(db_user, db_name, db_pass, INSERTS3)

def insertaTodo(db_user, db_name, db_pass):
    insertar(db_user, db_name, db_pass, INSERTS1)
    insertar(db_user, db_name, db_pass, ["pedidos.sql"])
    insertar(db_user, db_name, db_pass, INSERTS2)
    insertar(db_user, db_name, db_pass, INSERTS3)

def numTablas(db_user, db_name, db_pass):
    conn = mysql.connector.connect(host=DB_HOST, user=db_user, passwd=db_pass, database=db_name)
    cursor = conn.cursor()

    cursor.execute("select count(*) as tables from information_schema.tables where table_type = 'BASE TABLE' and table_schema not in ('information_schema', 'sys', 'performance_schema', 'mysql') and TABLE_SCHEMA = '{}' group by table_schema order by table_schema;".format(db_name))

    salida = cursor.fetchall()

    try:
        return(salida[0][0])
    except IndexError:
        return 0

def pruebaConexion(db_user, db_name, db_pass):
    try:
        mysql.connector.connect(host=DB_HOST, user=db_user, passwd=db_pass, database=db_name)
        return True
    except mysql.connector.errors.DatabaseError as e:
        print("\n")
        if e.errno == 1044:
            input("Error: Base de datos no accesible. Vuelve a intentarlo...")    
        elif e.errno == 1045:
            input("Error: Usuario o contraseña incorrectos. Vuelve a intentarlo...")
        elif e.errno == 2003:
            input("Error: Comprueba el estado del puerto. Vuelve a intentarlo...")
        else:
            print(e)

        os.system('clear')
        return False

def generacionCompleta(db_user, db_name, db_pass):
    os.system('clear')
    print(TITULO)

    if not(os.path.exists("./SQL") and os.path.isdir("./SQL")):
        os.mkdir("./SQL")

    start = timer()

    print("+--------------------------+")
    print("|    INICIANDO CREACIÓN    |")
    print("+--------------------------+")

    ejectutaFichero(db_user, db_name, db_pass, "./static/drop_triggers.sql", "¡Borrando triggers!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/drop_functions.sql", "¡Borrando funciones!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/drop_procedures.sql", "¡Borrando procesos!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/drop_events.sql", "¡Borrando eventos!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/drop_views.sql", "¡Borrando vistas!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/drop_tables.sql", "¡Borrando tablas!")
    try:
        ejectutaFichero(db_user, db_name, db_pass, "./static/drop_indices.sql", "¡Borrando indices!")   
    except:
        print("No es necesario borrar índices")
        pass

    ejectutaFichero(db_user, db_name, db_pass, "./static/create_tables.sql", "¡Creando tablas!")
    time.sleep(15)
    tablas = numTablas(db_user, db_name, db_pass)

    while(tablas < 18):
        ejectutaFichero(db_user, db_name, db_pass, "./static/create_tables.sql", "Creación de tablas en progreso...")
        time.sleep(15)
        tablas = numTablas(db_user, db_name, db_pass)

    ejectutaFichero(db_user, db_name, db_pass, "./static/create_triggers1.sql", "¡Primeros triggers creados!")   

    datasetsPlusInserta(db_user, db_name, db_pass)
    #insertaTodo(db_user, db_name, db_pass)

    ejectutaFichero(db_user, db_name, db_pass, "./static/create_triggers2.sql", "¡Resto de triggers creados!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/create_functions.sql", "¡Funciones creadas!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/create_procedures.sql", "¡Procesos creados!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/create_views.sql", "¡Vistas creadas!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/create_events.sql", "¡Eventos creados!")
    ejectutaFichero(db_user, db_name, db_pass, "./static/create_indices.sql", "¡Índices creados!")

    print("+--------------------------+")
    print("|       FIN  CREACIÓN      |")
    print("+--------------------------+")
    
    end = timer()

    print("Tiempo de ejecución: {}".format(timedelta(seconds=end-start)))
    input("GENERACIÓN FINALIZADA CON ÉXITO. Pulsa enter para cerrar.")
    os.system('clear')

def insertaDatasets(db_user, db_name, db_pass):
    # insertar(db_user, db_name, db_pass, INSERTS1)
    # insertar(db_user, db_name, db_pass, ["pedidos.sql"])
    # insertar(db_user, db_name, db_pass, INSERTS2)
    # insertar(db_user, db_name, db_pass, INSERTS3)

    insertar(db_user, db_name, db_pass, INSERTS1 + ["pedidos.sql"] + INSERTS2 + INSERTS3)

    # insertaFichero(db_user, db_name, db_pass, INSERTS1)
    # insertaFichero(db_user, db_name, db_pass, ["pedidos.sql"])
    # insertaFichero(db_user, db_name, db_pass, INSERTS2)
    # insertaFichero(db_user, db_name, db_pass, INSERTS3)

def informacionBBDD(db_user, db_name, db_pass):
    option = ""
    while option != "X":
        os.system('clear')
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
        print(" [X] Salir.")

        option = input("\nElige tu opción: ")

        if option in ["X", "x"]:
            return 0

        if option == "0":
            info.informacionTabla(db_user, db_name, db_pass)
        elif option == "1":
            info.nformacionVistas(db_user, db_name, db_pass)
        elif option == "2":
            info.informacionTriggers(db_user, db_name, db_pass)
        elif option == "3":
            info.informacionFuncion(db_user, db_name, db_pass)
        elif option == "4":
            info.informacionProcesos(db_user, db_name, db_pass)
        elif option == "5":
            info.informacionEventos(db_user, db_name, db_pass)
        else:
            input("\nOpción no válida...")


def inicioSesion():
    while True:
        os.system('clear')
        print(TITULO)
        db_user = input('Escribe tu usuario: ')
        db_name = input('Escribe tu database: ')
        db_pass = getpass.getpass('Contraseña: ')

        if pruebaConexion(db_user, db_name, db_pass):
            input("\n¡Sesión iniciada correctamente! Pulsa enter para volver al menú...")
            return [db_user, db_name, db_pass]

def menu():
    sesion = False
    option = ""
    while option != "X":
        os.system('clear')
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
            bbdd = inicioSesion()
            sesion = True
        elif (not sesion):
            input("\nEs necesario iniciar sesión primero...")
        else:
            if option == "1":
                continuar = input("\nEsta opción eliminará cualquier información existente en la BBDD. ¿Desea continuar? (S/n): ")
                if continuar in ["S", "s", ""]:
                    generacionCompleta(bbdd[0], bbdd[1], bbdd[2])
            elif option == "2":
                pass
            elif option == "3":
                continuar = input("\nEsta opción eliminará los datos de la BBDD. ¿Desea continuar? (S/n): ")
                if continuar in ["S", "s", ""]:
                    os.system('clear')
                    print(TITULO)
                    vaciatablas(bbdd[0], bbdd[1], bbdd[2])
                    input("\n¡Información borrada con éxito! Pulsa enter para volver al menú...")
            elif option == "4":
                continuar = input("\nRecuerda, antes de realizar este paso has de lanzar [3]. ¿Desea continuar? (S/n): ")
                if continuar in ["S", "s", ""]:
                    insertaDatasets(bbdd[0], bbdd[1], bbdd[2])
                    input("\n¡Información insertada con éxito! Pulsa enter para volver al menú...")
                    
            elif option == "5":
                informacionBBDD(bbdd[0], bbdd[1], bbdd[2])
            else:
                input("\nOpción no válida...")
    
    os.system('clear')


def main():
    menu()

if __name__ == "__main__":
	main()