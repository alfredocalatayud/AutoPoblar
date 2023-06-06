CREATE INDEX tarjeta_nif_cliente_index ON tarjeta_bancaria (nif_cliente);
CREATE INDEX transporte_nombre_index ON transporte (nombre);
CREATE INDEX usuario_mail ON usuario (mail(20));
CREATE INDEX valoracion_nif_cliente_index ON valoracion (nif_cliente);
CREATE INDEX valoracion_id_producto_index ON valoracion (id_producto);

CREATE INDEX linea_pedido_id_pedido ON linea_pedido (id_pedido);
CREATE INDEX linea_pedido_nif_vendedor ON linea_pedido (nif_vendedor);
CREATE INDEX linea_pedido_id_producto ON linea_pedido (id_producto);

CREATE INDEX lista_nif_cliente ON lista (nif_cliente);

CREATE INDEX mensaje_id_chat ON mensaje (id_chat);
CREATE INDEX mensaje_nif_usuario ON mensaje (nif_usuario);

CREATE INDEX pedido_nif_cliente ON pedido (nif_cliente);
CREATE INDEX pedido_fecha_pedido ON pedido (fecha_pedido);

CREATE INDEX producto_nif_vendedor ON producto (nif_vendedor);
CREATE INDEX producto_id_categoria ON producto (id_categoria);
CREATE INDEX producto_nombre ON producto (nombre);
CREATE INDEX producto_precio ON producto (precio);