CREATE VIEW VistaProductosOrdenadosPrecioDESC AS
SELECT *
FROM producto
ORDER BY precio DESC;

CREATE VIEW VistaProductosOrdenadosPrecioASC AS
SELECT *
FROM producto
ORDER BY precio ASC;

CREATE VIEW VistaProductosOrdenadosNombre AS
SELECT *
FROM producto
ORDER BY nombre ASC;

CREATE VIEW VistaClientesOrdenadosFechaAlta  AS
SELECT  mail, fecha_alta, c.*
FROM usuario u
JOIN cliente c where u.nif = c.nif 
ORDER BY u.fecha_alta;

CREATE VIEW VistaVendedoresOrdenadosFechaAlta AS
SELECT mail, fecha_alta, v.*
FROM usuario u
JOIN vendedor v where u.nif = v.nif 
ORDER BY u.fecha_alta;

CREATE VIEW VistaEmpleadosOrdenadosFechaAlta AS
SELECT mail, fecha_alta, e.*
FROM usuario u
JOIN empleado e where u.nif = e.nif 
ORDER BY u.fecha_alta;


CREATE VIEW VistaProductosMasVendidos AS
SELECT p.nombre AS Producto, SUM(lin_ped.cantidad) AS TotalVendidos
FROM linea_pedido lin_ped
JOIN producto p ON lin_ped.id_producto = p.id
WHERE lin_ped.estado = 'Entregado'
GROUP BY lin_ped.id_producto, p.nombre
ORDER BY TotalVendidos DESC
LIMIT 1;

CREATE VIEW VistaCategoriasMasVendidas AS
SELECT c.nombre AS Producto, SUM(lin_ped.cantidad) AS TotalVendidos
FROM linea_pedido lin_ped
JOIN producto p ON lin_ped.id_producto = p.id
JOIN categoria c ON p.id_categoria = c.id
WHERE lin_ped.estado = 'Entregado'
GROUP BY p.id_categoria, c.nombre
ORDER BY TotalVendidos DESC
LIMIT 1;