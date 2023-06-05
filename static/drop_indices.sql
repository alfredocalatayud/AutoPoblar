DROP INDEX IF EXISTS tarjeta_nif_cliente_index ON tarjeta_bancaria;
DROP INDEX IF EXISTS transporte_nombre_index ON transporte;
DROP INDEX IF EXISTS usuario_mail ON usuario;
DROP INDEX IF EXISTS valoracion_nif_cliente_index ON valoracion;
DROP INDEX IF EXISTS valoracion_id_producto_index ON valoracion;

DROP INDEX IF EXISTS linea_pedido_id_pedido ON linea_pedido;
DROP INDEX IF EXISTS linea_pedido_nif_vendedor ON linea_pedido;
DROP INDEX IF EXISTS linea_pedido_id_producto ON linea_pedido;

DROP INDEX IF EXISTS lista_nif_cliente ON lista;

DROP INDEX IF EXISTS mensaje_id_chat ON mensaje;
DROP INDEX IF EXISTS mensaje_nif_usuario ON mensaje;

DROP INDEX IF EXISTS pedido_nif_cliente ON pedido;
DROP INDEX IF EXISTS pedido_fecha_pedido ON pedido;

DROP INDEX IF EXISTS producto_nif_vendedor ON producto;
DROP INDEX IF EXISTS producto_id_categoria ON producto;
DROP INDEX IF EXISTS producto_nombre ON producto;
DROP INDEX IF EXISTS producto_precio ON producto;