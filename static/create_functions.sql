-- Calcula el precio total de una línea: Cantidad * Precio con impuestos
CREATE FUNCTION IF NOT EXISTS `total_linea`(idPedido INT, idLinea INT) RETURNS DECIMAL(10,2)
BEGIN
	DECLARE cantidadLinea TYPE OF linea_pedido.cantidad;
	DECLARE idProducto TYPE OF producto.id;
	DECLARE precioProducto TYPE OF producto.precio;
	SELECT lp.cantidad, id_producto INTO cantidadLinea, idProducto FROM linea_pedido lp WHERE id = idLinea AND id_pedido = idPedido;
	SELECT p.precio INTO precioProducto FROM producto p WHERE id = idProducto;
RETURN precioProducto*cantidadLinea;
END;

-- Calcula la base imponible de un pedido: Cantidad * Precio sin impuestos
CREATE FUNCTION IF NOT EXISTS `base_linea`(idPedido INT, idLinea INT) RETURNS DECIMAL(10,2)
BEGIN
	DECLARE porcentajeIVA TYPE OF producto.iva;
	DECLARE precioTotal TYPE OF linea_pedido.subtotal;
	SELECT total_linea(idPedido, idLinea) into precioTotal;
	SELECT p.iva INTO porcentajeIVA FROM producto p WHERE id = (SELECT lp.id_producto FROM linea_pedido lp WHERE lp.id = idLinea AND lp.id_pedido = idPedido);

RETURN precioTotal / (1+porcentajeIVA);
END;

-- Calcula la cantidad de impuestos de una línea: Base imponible * Tipo impositivo
CREATE FUNCTION IF NOT EXISTS `iva_linea`(idPedido INT, idLinea INT) RETURNS DECIMAL(10,2)
BEGIN
	DECLARE porcentajeIVA TYPE OF producto.iva;
	DECLARE precioTotal TYPE OF linea_pedido.subtotal;
	SELECT total_linea(idPedido, idLinea) INTO precioTotal;
	SELECT p.iva INTO porcentajeIVA FROM producto p WHERE id = (SELECT lp.id_producto FROM linea_pedido lp WHERE lp.id = idLinea AND lp.id_pedido = idPedido);
RETURN precioTotal / (1+porcentajeIVA) * porcentajeIVA;
END;

-- Calcula el ID de la siguiente línea que puede añadirse al pedido
-- (ID de la última línea del pedido + 1)
CREATE FUNCTION IF NOT EXISTS `id_linea_pedido`(idPedido INT, idCliente VARBINARY(255)) RETURNS INT
BEGIN
	DECLARE maxID int;
	SELECT IFNULL(MAX(lp.id), 0) INTO maxID FROM linea_pedido AS lp, pedido AS p WHERE lp.id_pedido = idPedido AND p.nif_cliente = idCliente;
RETURN (maxID + 1);
END;

-- Devuelve si el usuario indicado tiene un pedido con
-- líneas en estado cesta o no.
CREATE FUNCTION IF NOT EXISTS `tiene_cesta`(idCliente VARBINARY(255)) RETURNS BOOL
BEGIN
RETURN SELECT EXISTS (
  SELECT 1
  FROM linea_pedido AS lp, pedido AS p
  WHERE lp.id_pedido = p.id
    AND p.nif_cliente = idCliente
    AND lp.estado = 'Cesta'
);
END;

-- Devuelve el ID del pedido que representa la cesta del usuario indicado.
CREATE FUNCTION IF NOT EXISTS `obtener_id_cesta`(idCliente VARBINARY(255)) RETURNS INT
BEGIN
	DECLARE idCesta TYPE OF pedido.id;
	SELECT p.id INTO idCesta
		FROM pedido AS p
		WHERE p.nif_cliente = idCliente
		AND EXISTS (
			SELECT 1
			FROM linea_pedido AS lp
			WHERE lp.id_pedido = p.id AND lp.estado = 'Cesta'
		)
		LIMIT 1;
	RETURN idCesta;
END;

-- Devuelve la relevancia en una escala de 1 (mal) a 5 (excelente)
CREATE FUNCTION IF NOT EXISTS `calcular_relevancia`(idProducto INT) RETURNS FLOAT
BEGIN
	-- Declaración de variables
	DECLARE ventasUltimoMes int;
	DECLARE ventasNormalizadas int;
	DECLARE mediaValoracionClientes float;
	DECLARE mediaValoracionesUltimoMes float;
	DECLARE resultado float;
	-- Recogida de datos necesarios para la calificación
	SELECT sum(cantidad) INTO ventasUltimoMes 
		FROM linea_pedido lp, pedido p 
		WHERE lp.id_pedido = p.id 
			AND lp.id_producto = idProducto AND lp.estado != 'Cesta' AND lp.estado != 'Cancelado' AND lp.estado != 'Devuelto' 
			AND p.fecha_pedido >= now() - INTERVAL 1 MONTH
		GROUP BY lp.id_producto ;
	SELECT SUM(v.calificacion) / COUNT(v.calificacion) INTO mediaValoracionClientes FROM valoracion v, pedido p 
			WHERE v.id_producto = idProducto AND p.fecha_pedido >= now() - INTERVAL 1 MONTH;
	SELECT SUM(v.calificacion) / COUNT(v.calificacion) INTO mediaValoracionesUltimoMes FROM valoracion v 
			WHERE v.id_producto = idProducto;
	-- Normalizar el número de ventas de 1 a 5
	SELECT CASE
  		when (0 < ventasUltimoMes and ventasUltimoMes < 100) then 1
  		when (99 < ventasUltimoMes and ventasUltimoMes < 200) then 2
  		when (199 < ventasUltimoMes and ventasUltimoMes < 300) then  3
  		when (299 < ventasUltimoMes and ventasUltimoMes < 400) then  4
  		when (400 < ventasUltimoMes) then 5
  		END INTO ventasNormalizadas;
  	-- Calcular la relevancia
  	SELECT 0.25*mediaValoracionClientes + 0.25*mediaValoracionesUltimoMes + 0.5*ventasNormalizadas INTO resultado;
  	-- Asegurar que la función no devuelve null
  	IF resultado IS NULL THEN 
  		SELECT 0 INTO resultado;
  	END IF;
	RETURN resultado;
END;
