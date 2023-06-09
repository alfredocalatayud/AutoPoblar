import bcrypt
import sys
import platform
from tabulate import tabulate
import mysql.connector
import os

if sys.platform.startswith('win'):
    LIMPIAR = "cls"
else:
    LIMPIAR = "clear"

DB_HOST = 'bbdd.dlsi.ua.es'
TITULO = """888b. w                                w    8                     db           w         888b.       8    8           
8wwwP w .d88b 8d8b. Yb  dP .d88b 8d8b. w .d88 .d8b.    .d88      dPYb   8   8 w8ww .d8b. 8  .8 .d8b. 88b. 8 .d88 8d8b 
8   b 8 8.dP' 8P Y8  YbdP  8.dP' 8P Y8 8 8  8 8' .8    8  8     dPwwYb  8b d8  8   8' .8 8wwP' 8' .8 8  8 8 8  8 8P   
888P' 8 `Y88P 8   8   YP   `Y88P 8   8 8 `Y88 `Y8P'    `Y88    dP    Yb `Y8P8  Y8P `Y8P' 8     `Y8P' 88P' 8 `Y88 8\n"""

def informacionTabla(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME, TABLE_ROWS, DATA_LENGTH, DATA_FREE, CREATE_TIME, UPDATE_TIME \
                    FROM information_schema.tables \
                    WHERE table_schema = '{}' \
                    AND TABLE_type = 'BASE TABLE';".format(conn.database))
    
    resultado = cursor.fetchall()

    os.system(LIMPIAR)
    print(TITULO)

    print("+----------------------------+")
    print("|  Información sobre tablas  |")
    print("+----------------------------+\n")

    print(tabulate(resultado, headers=["Nombre", "Número de filas", "Almacenamiento usado", "Almacenamiento libre", "Fecha de creación", "Fecha de última modificación"], tablefmt='psql'))

    print("\nNúmero de tablas: {}".format(len(resultado)))

    input("\nPulsa enter para volver al menú...")

def informacionVistas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME \
                    FROM information_schema.tables \
                    WHERE table_schema = '{}' \
                    and table_type = 'VIEW';".format(conn.database))
    
    resultado = cursor.fetchall()

    os.system(LIMPIAR)
    print(TITULO)

    print("+----------------------------+")
    print("|  Información sobre vistas  |")
    print("+----------------------------+\n")

    print(tabulate(resultado, headers=["Nombre de la vista"], tablefmt='psql'))

    print("\nNúmero de vistas: {}".format(len(resultado)))

    input("\nPulsa enter para volver al menú...")

def informacionTriggers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT TRIGGER_name, EVENT_manipulation, event_object_table, ACTION_timing, created \
                    FROM information_schema.triggers \
                    WHERE trigger_schema = '{}';".format(conn.database))
    
    resultado = cursor.fetchall()

    os.system(LIMPIAR)
    print(TITULO)

    print("+----------------------------------+")
    print("|  Información sobre disparadores  |")
    print("+----------------------------------+\n")

    print(tabulate(resultado, headers=["Nombre del trigger", "Evento disparador", "Tabla", "Momento de actuación", "Fecha de creación"], tablefmt='psql'))

    print("\nNúmero de disparadores: {}".format(len(resultado)))

    input("\nPulsa enter para volver al menú...")

def informacionFuncion(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT SPECIFIC_NAME, CREATED, LAST_altered \
                    FROM information_schema.routines \
                    WHERE ROUTINE_schema = '{}' \
                    AND ROUTINE_type = 'FUNCTION'".format(conn.database))
    
    resultado = cursor.fetchall()

    os.system(LIMPIAR)
    print(TITULO)

    print("+-------------------------------+")
    print("|  Información sobre funciones  |")
    print("+-------------------------------+\n")

    print(tabulate(resultado, headers=["Nombre de la función", "Fecha de creación", "Fecha última modificación"], tablefmt='psql'))

    print("\nNúmero de funciones: {}".format(len(resultado)))

    input("\nPulsa enter para volver al menú...")

def informacionProcesos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT SPECIFIC_NAME, CREATED, LAST_altered \
                    FROM information_schema.routines \
                    WHERE ROUTINE_schema = '{}' \
                    AND ROUTINE_type = 'PROCEDURE'".format(conn.database))
    
    resultado = cursor.fetchall()

    os.system(LIMPIAR)
    print(TITULO)

    print("+------------------------------+")
    print("|  Información sobre procesos  |")
    print("+------------------------------+\n")

    print(tabulate(resultado, headers=["Nombre del proceso", "Fecha de creación", "Fecha última modificación"], tablefmt='psql'))

    print("\nNúmero de procesos: {}".format(len(resultado)))

    input("\nPulsa enter para volver al menú...")

def informacionEventos(conn):    
    cursor = conn.cursor()
    cursor.execute("SELECT event_name, created, last_altered \
                    FROM information_schema.events \
                    WHERE event_schema = '{}';".format(conn.database))
    
    resultado = cursor.fetchall()

    os.system(LIMPIAR)
    print(TITULO)

    print("+------------------------------+")
    print("|  Información sobre eventos   |")
    print("+------------------------------+\n")

    print(tabulate(resultado, headers=["Nombre del evento", "Fecha de creación", "Fecha última modificación"], tablefmt='psql'))

    print("\nNúmero de eventos: {}".format(len(resultado)))

    input("\nPulsa enter para volver al menú...")

def getVendedor(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT convert(aes_decrypt(usua.mail, SHA2('abcdefghijklmnopqrstuvwx', 512)) using utf8) AS email, convert(aes_decrypt(usua.nif, SHA2('abcdefghijklmnopqrstuvwx', 512)) using utf8) AS nif, '1234' AS pwd \
                    FROM usuario usua, vendedor clie \
                    WHERE usua.nif = clie.nif \
                    ORDER BY RAND() LIMIT 3;")
    
    resultado = cursor.fetchall()

    pwd = '1234'
    salt = bcrypt.gensalt()
    contrasenya = bcrypt.hashpw(pwd.encode(), salt)

    os.system(LIMPIAR)
    print(TITULO)
    print("\nCargando vendedores...")
    for pers in resultado:
        query = "UPDATE usuario \
                 SET contrasenya = \"{}\" \
                 WHERE nif = aes_encrypt('{}', SHA2('abcdefghijklmnopqrstuvwx', 512));".format(contrasenya.decode('utf-8'), pers[1])

        cursor.execute(query)
        cursor.execute("commit")

    os.system(LIMPIAR)
    print(TITULO)
    print("+---------------------------+")
    print("|  Información vendedores   |")
    print("+---------------------------+\n")

    print(tabulate(resultado, headers=["Email", "NIF", "Contraseña"], tablefmt='psql'))

    input("\nPulsa enter para volver al menú...")

def getCliente(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT convert(aes_decrypt(usua.mail, SHA2('abcdefghijklmnopqrstuvwx', 512)) using utf8) AS email, convert(aes_decrypt(usua.nif, SHA2('abcdefghijklmnopqrstuvwx', 512)) using utf8) AS nif, '1234' AS pwd \
                    FROM usuario usua, cliente clie \
                    WHERE usua.nif = clie.nif \
                    ORDER BY RAND() LIMIT 3;")
    
    resultado = cursor.fetchall()

    pwd = '1234'
    salt = bcrypt.gensalt()
    contrasenya = bcrypt.hashpw(pwd.encode(), salt)

    os.system(LIMPIAR)
    print(TITULO)
    print("\nCargando clientes...")
    for pers in resultado:
        query = "UPDATE usuario \
                 SET contrasenya = \"{}\" \
                 WHERE nif = aes_encrypt('{}', SHA2('abcdefghijklmnopqrstuvwx', 512));".format(contrasenya.decode('utf-8'), pers[1])

        cursor.execute(query)
        cursor.execute("commit")

    os.system(LIMPIAR)
    print(TITULO)
    print("+-------------------------+")
    print("|  Información clientes   |")
    print("+-------------------------+\n")

    print(tabulate(resultado, headers=["Email", "NIF", "Contraseña"], tablefmt='psql'))

    input("\nPulsa enter para volver al menú...")

def getEmpleado(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT convert(aes_decrypt(usua.mail, SHA2('abcdefghijklmnopqrstuvwx', 512)) using utf8) AS email, convert(aes_decrypt(usua.nif, SHA2('abcdefghijklmnopqrstuvwx', 512)) using utf8) AS nif, '1234' AS pwd \
                    FROM usuario usua, empleado clie \
                    WHERE usua.nif = clie.nif \
                    ORDER BY RAND() LIMIT 3;")
    
    resultado = cursor.fetchall()

    pwd = '1234'
    salt = bcrypt.gensalt()
    contrasenya = bcrypt.hashpw(pwd.encode(), salt)

    os.system(LIMPIAR)
    print(TITULO)
    print("\nCargando empleados...")
    for pers in resultado:
        query = "UPDATE usuario \
                 SET contrasenya = \"{}\" \
                 WHERE nif = aes_encrypt('{}', SHA2('abcdefghijklmnopqrstuvwx', 512));".format(contrasenya.decode('utf-8'), pers[1])

        cursor.execute(query)
        cursor.execute("commit")

    os.system(LIMPIAR)
    print(TITULO)
    print("+--------------------------+")
    print("|  Información empleados   |")
    print("+--------------------------+\n")

    print(tabulate(resultado, headers=["Email", "NIF", "Contraseña"], tablefmt='psql'))

    input("\nPulsa enter para volver al menú...")

    