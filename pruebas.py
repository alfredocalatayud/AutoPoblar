import requests
import io
import mysql.connector


DB_HOST = 'bbdd.dlsi.ua.es'

# define a function to retrieve and display an image based on the selected category

def numTablas():
    conn = mysql.connector.connect(host=DB_HOST, user='gi_acs128', passwd='Caramelos1998', database='gi_acs128')
    cursor = conn.cursor()

    cursor.execute("select count(*) as tables from information_schema.tables where table_type = 'BASE TABLE' and table_schema not in ('information_schema', 'sys', 'performance_schema', 'mysql') and TABLE_SCHEMA = '{}' group by table_schema order by table_schema;".format('gi_acs128'))

    salida = cursor.fetchall()

    print(salida[0][0])


if __name__ == '__main__':
    numTablas()













