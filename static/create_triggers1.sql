CREATE TRIGGER IF NOT EXISTS producto_au_trigger
AFTER UPDATE ON producto FOR EACH ROW 
BEGIN 
	-- Si cambia el precio del producto, cambiar precio linped con estado cesta
	IF old.precio <> new.precio THEN
		UPDATE linea_pedido  
		SET precio = new.precio
		WHERE id_producto = new.id AND estado = 'Cesta';
	END IF;
	
	-- Si cambia el iva del producto, cambiar iva linped con estado cesta
	IF old.iva <> new.iva THEN
		UPDATE linea_pedido  
		SET iva = new.iva
		WHERE id_producto = new.id AND estado = 'Cesta';
	END IF;
	
	-- Si se desactiva el producto, quitar productos de linped con estado cesta
	IF new.activo = 0 AND old.activo <> new.activo THEN
		DELETE FROM linea_pedido
		WHERE id_producto = new.id AND estado = 'Cesta';
	END IF;	
END;

CREATE TRIGGER IF NOT EXISTS vendedor_au_trigger
AFTER UPDATE on usuario for each ROW 
BEGIN 
	-- Si se desactiva el vendedor, desactivar productos asociados (si está activo o no lo tengo que mirar en tabla usuario)
	if new.activo = 0 AND old.activo <> new.activo THEN
		UPDATE producto
		SET activo = 0
		WHERE nif_vendedor = new.nif;
	end if;	
END;

CREATE TRIGGER IF NOT EXISTS linea_pedido_au_trigger
AFTER UPDATE on linea_pedido for each ROW 
BEGIN 
	if new.estado <> old.estado THEN 
		-- Si linped confirmado, restamos stock producto y ponemos fecha de pedido a la actual
		if new.estado = 'Confirmado' THEN			

			UPDATE producto 
			SET stock = stock - new.cantidad
			WHERE id = new.id_producto;
		
			UPDATE pedido 
			SET fecha_pedido = CURRENT_DATE()
			WHERE id = new.id_pedido;
			
			
		end if;
		
		-- Si linped devuelto, sumamos stock
		if new.estado = 'Devuelto' THEN
			UPDATE producto 
			SET stock = stock + new.cantidad
			WHERE id = new.id_producto;
			
		end if;
		
		
	end if;
END;

CREATE TRIGGER IF NOT EXISTS linea_pedido_bu_trigger
BEFORE UPDATE on linea_pedido for each ROW
BEGIN
	-- Actualizamos la base, el subtotal y el total del pedido
	if new.precio <> old.precio OR new.cantidad <> old.cantidad OR new.iva <> old.iva THEN
		set new.base = (new.precio * new.cantidad) / (1 + new.iva);
		set new.subtotal = new.precio * new.cantidad;

		UPDATE pedido 
		SET total = total + new.subtotal - old.subtotal
		WHERE pedido.id = new.id_pedido;
	end if;
END;

CREATE TRIGGER IF NOT EXISTS linea_pedido_ai_trigger
AFTER INSERT ON linea_pedido for each ROW
BEGIN
	DECLARE costes_envio_producto TYPE OF pedido.coste_envio;

	SELECT costes_envio from producto where id = new.id_producto into costes_envio_producto;

	UPDATE pedido SET total = (total + new.subtotal), coste_envio = (coste_envio + costes_envio_producto) WHERE id = new.id_pedido;
END;

CREATE TRIGGER IF NOT exists linea_pedido_bi_trigger
BEFORE INSERT ON linea_pedido for each ROW
BEGIN
	DECLARE precio_val TYPE OF linea_pedido.precio;
	DECLARE iva_val TYPE OF linea_pedido.iva;

	SELECT precio, iva FROM producto WHERE producto.id = new.id_producto into precio_val, iva_val;
	
	set new.precio = precio_val;
	set new.iva = iva_val;
	set new.base = (new.precio * new.cantidad) / (1 + new.iva);
	set new.subtotal = new.precio * new.cantidad;
END;

CREATE TRIGGER IF NOT EXISTS linea_pedido_ad_trigger
AFTER DELETE on linea_pedido for each ROW 
BEGIN 
	DECLARE costes_envio_producto TYPE OF pedido.coste_envio;
	if (select count(*) FROM linea_pedido WHERE id_pedido = old.id_pedido) = 0 THEN 
		DELETE FROM pedido
		WHERE id = old.id_pedido;
	ELSE 
		SELECT costes_envio from producto where id = old.id_producto into costes_envio_producto;
		UPDATE pedido SET total = (total - old.subtotal), coste_envio = (coste_envio - costes_envio_producto) WHERE id = old.id_pedido;

	end if;	
END;
