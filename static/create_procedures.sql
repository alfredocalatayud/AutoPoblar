CREATE PROCEDURE IF NOT EXISTS dar_alta_cliente(IN aux_nif VARCHAR(256), IN aux_mail BLOB, IN aux_contrasenya VARCHAR(150), IN aux_telefono VARCHAR(50), IN aux_activo TINYINT(1), IN aux_nombre VARCHAR(50), in aux_apellidos VARCHAR(50), in aux_fecha_nacimiento DATE)
BEGIN
	START TRANSACTION;
		INSERT INTO usuario (nif, mail, contrasenya, telefono, activo) VALUES (aux_nif, aux_mail, aux_contrasenya, aux_telefono, aux_activo);
		INSERT INTO cliente (nif, nombre, apellidos, fecha_nacimiento) VALUES (aux_nif, aux_nombre, aux_apellidos, aux_fecha_nacimiento);
	COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS dar_alta_vendedor(IN aux_nif VARCHAR(256), IN aux_mail BLOB, IN aux_contrasenya VARCHAR(150), IN aux_telefono VARCHAR(50), IN aux_activo TINYINT(1), IN aux_razon_social VARCHAR(50), IN aux_documento_acreditativo_alta VARCHAR(50), IN aux_cuenta_bancaria BLOB, IN aux_verificado TINYINT(1), IN aux_logo BLOB)
BEGIN
	START TRANSACTION;
		INSERT INTO usuario (nif, mail, contrasenya, telefono, activo) VALUES (aux_nif, aux_mail, aux_contrasenya, aux_telefono, aux_activo);
		INSERT INTO vendedor (nif, razon_social, documento_acreditativo_alta, cuenta_bancaria, verificado, logo) VALUES (aux_nif, aux_razon_social, aux_documento_acreditativo_alta, aux_cuenta_bancaria, aux_verificado, aux_logo);
	COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS dar_alta_empleado(IN aux_nif VARCHAR(256), IN aux_mail BLOB, IN aux_contrasenya VARCHAR(150), IN aux_telefono VARCHAR(50), IN aux_activo TINYINT(1), IN aux_nombre VARCHAR(50), IN aux_apellidos VARCHAR(50), IN aux_fecha_nacimiento DATE, IN aux_numero_seguridad_social VARCHAR(50), IN aux_cargo_empresa VARCHAR(50))
BEGIN
	START TRANSACTION;
		INSERT INTO usuario (nif, mail, contrasenya, telefono, activo) VALUES (aux_nif, aux_mail, aux_contrasenya, aux_telefono, aux_activo);
		INSERT INTO empleado (nif, nombre, apellidos, fecha_nacimiento, numero_seguridad_social, cargo_empresa) VALUES (aux_nif, aux_nombre, aux_apellidos, aux_fecha_nacimiento, aux_numero_seguridad_social, aux_cargo_empresa);
	COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS dar_alta_producto(IN aux_nombre VARCHAR(50), IN aux_descripcion VARCHAR(2500), IN aux_id_categoria INT(11), IN aux_nif_vendedor VARCHAR(256), IN aux_precio DECIMAL(10.2), IN aux_costes_envio DECIMAL(10.2), IN aux_iva DECIMAL(5.2), IN aux_stock INT(11), IN aux_plazo_devolucion INT(11), IN aux_dimensiones VARCHAR(12), IN aux_peso DECIMAL(5.2), IN aux_url_imagen VARCHAR(500), IN aux_restric_edad INT(11), IN aux_activo TINYINT(1), IN aux_relevancia INT(11))
BEGIN
	START TRANSACTION;
		INSERT INTO producto (nombre, descripcion, id_categoria, nif_vendedor, precio, costes_envio, iva, stock, plazo_devolucion, dimensiones, peso, url_imagen, restrict_edad, activo) VALUES (aux_nombre, aux_descripcion, aux_id_categoria, aux_nif_vendedor, aux_precio, aux_costes_envio, aux_iva, aux_stock, aux_plazo_devolucion, aux_dimensiones, aux_peso, aux_url_imagen, aux_restric_edad, aux_activo, aux_relevancia);
	COMMIT;
END;

CREATE PROCEDURE IF NOT EXISTS crear_linped(IN aux_cantidad INT(11), IN aux_id_producto INT(11), IN aux_nif_cliente VARCHAR(256))
BEGIN
	DECLARE cesta BOOLEAN;
	DECLARE aux_id_cesta, aux_id_linped INT;
	DECLARE aux_precio, aux_iva DECIMAL(10,2);
	
	SELECT tiene_cesta(aux_nif_cliente) INTO cesta;
	SELECT precio, iva INTO aux_precio, aux_iva FROM producto WHERE id = aux_id_producto;
	
	IF (cesta) THEN
		
		SELECT obtener_id_cesta(aux_nif_cliente) INTO aux_id_cesta;
		SELECT id_linea_pedido(aux_id_cesta, aux_nif_cliente) INTO aux_id_linped;
		
		INSERT INTO linea_pedido (id, cantidad, precio, base, iva, subtotal, estado, fecha_envio, fecha_recepcion, id_producto, id_pedido) VALUES (aux_id_linped, aux_cantidad, aux_precio, 0.0, aux_iva, 0.0, 'Cesta', NULL, NULL, aux_id_producto, aux_id_cesta);
		
	ELSE
		INSERT INTO pedido (total, fecha_pedido, coste_envio, tiempo_envio, nif_cliente, nif_transporte, id_dir_envio, id_dir_fact, num_tarjeta_bancaria) VALUES (0.0, NULL, 0.0, NULL, aux_nif_cliente, NULL, NULL, NULL, NULL);
		
		SELECT MAX(id) INTO aux_id_cesta FROM pedido WHERE nif_cliente = aux_nif_cliente;
		SELECT id_linea_pedido(aux_id_cesta, aux_nif_cliente) INTO aux_id_linped;
		
		INSERT INTO linea_pedido (id, cantidad, precio, base, iva, subtotal, estado, fecha_envio, fecha_recepcion, id_producto, id_pedido) VALUES (aux_id_linped, aux_cantidad, aux_precio, 0.0, aux_iva, 0.0, 'Cesta', NULL, NULL, aux_id_producto, aux_id_cesta);
	END IF;
END;

CREATE PROCEDURE IF NOT EXISTS realizar_compra(IN aux_nif_cliente VARCHAR(256))
BEGIN
	DECLARE cesta BOOLEAN;
	DECLARE aux_id_cesta INT;

	SELECT tiene_cesta(aux_nif_cliente) INTO cesta;
	
	IF (cesta = TRUE) THEN 

		START TRANSACTION;
			SELECT obtener_id_cesta(aux_nif_cliente) INTO aux_id_cesta;
			UPDATE linea_pedido, pedido SET estado = 'Pendiente' WHERE estado='Cesta' AND id_pedido = aux_id_cesta AND aux_id_cesta = pedido.id AND linea_pedido.id_pedido = pedido.id AND nif_cliente = aux_nif_cliente;
		COMMIT;

	END IF;
END;
