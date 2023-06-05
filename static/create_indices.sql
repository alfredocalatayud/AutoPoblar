CREATE if not EXISTS INDEX tarjeta_nif_cliente_index ON tarjeta_bancaria (nif_cliente);
CREATE if not EXISTS INDEX transporte_nombre_index ON transporte (nombre);
CREATE if not EXISTS INDEX usuario_mail ON usuario (mail(20));
CREATE if not EXISTS INDEX valoracion_nif_cliente_index ON valoracion (nif_cliente);
CREATE if not EXISTS INDEX valoracion_id_producto_index ON valoracion (id_producto);

CREATE if not EXISTS INDEX linea_pedido_id_pedido ON linea_pedido (id_pedido);
CREATE if not EXISTS INDEX linea_pedido_nif_vendedor ON linea_pedido (nif_vendedor);
CREATE if not EXISTS INDEX linea_pedido_id_producto ON linea_pedido (id_producto);

CREATE if not EXISTS INDEX lista_nif_cliente ON lista (nif_cliente);

CREATE if not EXISTS INDEX mensaje_id_chat ON mensaje (id_chat);
CREATE if not EXISTS INDEX mensaje_nif_usuario ON mensaje (nif_usuario);

CREATE if not EXISTS INDEX pedido_nif_cliente ON pedido (nif_cliente);
CREATE if not EXISTS INDEX pedido_fecha_pedido ON pedido (fecha_pedido);

CREATE if not EXISTS INDEX producto_nif_vendedor ON producto (nif_vendedor);
CREATE if not EXISTS INDEX producto_id_categoria ON producto (id_categoria);
CREATE if not EXISTS INDEX producto_nombre ON producto (nombre);
CREATE if not EXISTS INDEX producto_precio ON producto (precio);