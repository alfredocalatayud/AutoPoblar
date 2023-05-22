# AutoPoblar

AutoPoblar es una herramienta diseñada para poblar la BBDD de Tierra de Alicante, proyecto de la asignatura Gestión de la Información en la Universidad de Alicante.

## Instalación

Es necesario tener instalado [Python3](https://www.python.org/downloads/) en vuestro equipo.

Usar el gestor de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar los siguientes paquetes:

```bash
pip install faker
pip install progress
pip install mysql-connector-python
```

## Ejecución

Para ejecutar AutoPoblar debemos lanzar el siguiente comando:

```python
python3 AutoPoblar.py
```

Dependiente de la versión de Python que utilices deberás usar el comando python ó python3.

## Salida

Una ejecución normal de AutoPoblar debe tener el siguiente aspecto:

```python
MacBook-Pro-de-Alfredo:AutoPoblar alfredocalatayud$ python3 AutoPoblar.py 
Escribe tu usuario: gi_acs128
Escribe tu database: gi_acs128
Contraseña: 
¿Desea vaciar tablas? (S/n): 
¿Generar datasets? (s/N): S
¿Generar NIFs? (s/N): 
| -------------------------|
| INICIO BORRADO DE TABLAS |
| -------------------------|
Procesando |################################| 18/18
| -----------------------------|
| BORRADO DE TABLAS FINALIZADO |
| -----------------------------|
Generando usuarios: |################################| 1000000/1000000
Generando categorías: |################################| 190/190
Generando clientes: |################################| 200/200
Generando direcciones: |################################| 1000000/1000000
Generando empleados: |################################| 200/200
Generando vendedores: |################################| 200/200
Generando productos: |################################| 190/190
Generando tarjetas: |################################| 200/200
Generando listas: |################################| 2000/2000
Generando chats archivados: |################################| 200/200
Generando chats: |################################| 200/200
Generando transportes: |################################| 20/20
Generando valoraciones: |################################| 300/300
| -------------------------|
| INICIO INSERTS EN TABLAS |
| -------------------------|
Insertando usuarios.sql...
Procesando |################################| 500/500
Insertando categorias.sql...
Procesando |################################| 1/1
Insertando clientes.sql...
Procesando |################################| 1/1
Insertando direcciones.sql...
Procesando |################################| 500/500
Insertando empleados.sql...
Procesando |################################| 1/1
Insertando vendedores.sql...
Procesando |################################| 1/1
Insertando productos.sql...
Procesando |################################| 1/1
Insertando transportes.sql...
Procesando |################################| 1/1
Insertando tarjetas.sql...
Procesando |################################| 2/2
| -----------------------------|
| INSERTS EN TABLAS FINALIZADO |
| -----------------------------|
Generando pedidos: |################################| 200/200
| -------------------------|
| INICIO INSERTS EN TABLAS |
| -------------------------|
Insertando pedidos.sql...
Procesando |################################| 2/2
| -----------------------------|
| INSERTS EN TABLAS FINALIZADO |
| -----------------------------|
Generando lineas de pedidos: |################################| 2105/2105
| -------------------------|
| INICIO INSERTS EN TABLAS |
| -------------------------|
Insertando listas.sql...
Procesando |################################| 1/1
Insertando lineas_pedidos.sql...
Procesando |################################| 20/20
Insertando chats.sql...
Procesando |################################| 1/1
Insertando chats_archivados.sql...
Procesando |################################| 1/1
Insertando valoraciones.sql...
Procesando |################################| 1/1
| -----------------------------|
| INSERTS EN TABLAS FINALIZADO |
| -----------------------------|
Generando listas de productos: |################################| 2000/2000
Generando mensajes archivados: |################################| 200/200
Generando mensajes: |################################| 200/200
| -------------------------|
| INICIO INSERTS EN TABLAS |
| -------------------------|
Insertando listas_producto.sql...
Procesando |################################| 21/21
Insertando mensajes.sql...
Procesando |################################| 2/2
Insertando mensajes_archivados.sql...
Procesando |################################| 2/2
| -----------------------------|
| INSERTS EN TABLAS FINALIZADO |
| -----------------------------|
GENERACIÓN FINALIZADA CON ÉXITO. Pulsa enter para cerrar.
```

Dependiente de la versión de Python que utilices deberás usar el comando python ó python3.

## Dudas

Tienen ustedes mi teléfono para cualquier consulta :)

## License

[MIT](https://choosealicense.com/licenses/mit/)
