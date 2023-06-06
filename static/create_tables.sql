set foreign_key_checks = 0;

CREATE OR REPLACE TABLE usuario ( -- Revisado
    nif VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    mail blob NOT NULL, -- Encriptado AES habilitado
    contrasenya varchar(150) NOT NULL, 
    telefono varchar(50) NOT NULL, 
    activo boolean NOT NULL, 
    fecha_alta date,
    CONSTRAINT pk_usuario 
        PRIMARY KEY (nif), 
    CONSTRAINT ak_usuario 
        UNIQUE (mail)
);

CREATE OR REPLACE TABLE vendedor ( -- Revisado
    nif VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    razon_social varchar(50) NOT NULL, 
    documento_acreditativo_alta varchar(50), 
    cuenta_bancaria blob NOT NULL, -- Encriptado AES habilitado
    verificado boolean NOT NULL, 
    logo blob, -- Fichero multimedia
    CONSTRAINT pk_vendedor 
        PRIMARY KEY (nif), 
    CONSTRAINT ak_vendedor 
        UNIQUE (razon_social), 
    CONSTRAINT fk_vendedor_usuario
        FOREIGN KEY (nif) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE
);

CREATE or REPLACE TABLE cliente ( -- Revisado
    nif VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    nombre varchar(50) NOT NULL, 
    apellidos varchar(50) NOT NULL, 
    fecha_nacimiento date NOT NULL, 
    CONSTRAINT pk_cliente 
        PRIMARY KEY (nif), 
    CONSTRAINT fk_cliente_usuario
        FOREIGN KEY (nif) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE
);

CREATE OR REPLACE TABLE categoria ( 
    id int UNSIGNED NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    categoria_padre int UNSIGNED,
    imagen blob,  -- Fichero multimedia
    CONSTRAINT pk_categoria 
        PRIMARY KEY (id),
    CONSTRAINT ak_categoria
        UNIQUE KEY (nombre),
    CONSTRAINT fk_categoria_subcategoria 
        FOREIGN KEY (categoria_padre) 
        REFERENCES categoria(id) 
);

CREATE OR REPLACE TABLE direccion ( -- Revisado
    id int UNSIGNED NOT NULL AUTO_INCREMENT, 
    nif_usuario VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    calle varchar(50) NOT NULL, 
    numero varchar(50) NOT NULL, 
    puerta varchar(50) NOT NULL, 
    localidad varchar(50) NOT NULL, 
    codigo_postal varchar(5) NOT NULL, 
    pais varchar(50) NOT NULL, 
    CONSTRAINT pk_direccion 
        PRIMARY KEY (id), 
    CONSTRAINT fk_direccion_usuario
        FOREIGN KEY (nif_usuario) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE
);

CREATE OR REPLACE TABLE empleado ( -- Revisado
    nif VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    nombre varchar(50) NOT NULL, 
    apellidos varchar(50) NOT NULL, 
    fecha_nacimiento date NOT NULL, 
    numero_seguridad_social varchar(50) NOT NULL, 
    cargo_empresa varchar(50), 
    CONSTRAINT pk_empleado 
        PRIMARY KEY (nif), 
    CONSTRAINT ak_empleado
        UNIQUE KEY (numero_seguridad_social),
    CONSTRAINT fk_empleado_usuario
        FOREIGN KEY (nif) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE
);

CREATE OR REPLACE TABLE producto ( -- Revisado
    id int UNSIGNED NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    descripcion varchar(2500) NOT NULL, 
    id_categoria int UNSIGNED NOT NULL, 
    nif_vendedor VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    precio decimal(10, 2) NOT NULL, 
    costes_envio decimal(10, 2), 
    iva decimal(5, 2) NOT NULL, 
    stock int NOT NULL, 
    plazo_devolucion INT, 
    dimensiones varchar(12), 
    peso decimal(5, 2), 
    url_imagen varchar(500), 
    restric_edad int, 
    activo boolean NOT NULL default 1, 
    relevancia int default 0,
    CONSTRAINT pk_producto 
        PRIMARY KEY (id), 
    CONSTRAINT fk_producto_vendedor 
        FOREIGN KEY (nif_vendedor) 
        REFERENCES vendedor(nif)
        ON UPDATE CASCADE, 
    CONSTRAINT fk_producto_categoria 
        FOREIGN KEY (id_categoria) 
        REFERENCES categoria(id)
);

CREATE OR REPLACE TABLE lista ( -- Revisado
    id int UNSIGNED NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    descripcion varchar(150), 
    nif_cliente VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    CONSTRAINT pk_lista 
        PRIMARY KEY (id), 
    CONSTRAINT ak_lista 
        UNIQUE KEY (nombre, nif_cliente), 
    CONSTRAINT fk_lista_cliente 
        FOREIGN KEY (nif_cliente) 
        REFERENCES cliente(nif)
        ON UPDATE CASCADE
);

CREATE OR REPLACE TABLE producto_lista ( -- Revisado
    id_producto int UNSIGNED NOT NULL, 
    id_lista int UNSIGNED NOT NULL, 
    CONSTRAINT pk_producto_lista 
        PRIMARY KEY (id_producto, id_lista), 
    CONSTRAINT fk_producto_lista_producto 
        FOREIGN KEY (id_producto) 
        REFERENCES producto(id), 
    CONSTRAINT fk_producto_lista_lista 
        FOREIGN KEY (id_lista) 
        REFERENCES lista(id) 
        ON DELETE CASCADE
);

CREATE OR REPLACE TABLE valoracion ( -- Revisado
    id int UNSIGNED NOT NULL AUTO_INCREMENT, 
    calificacion int NOT NULL, 
    titulo varchar(50), 
    cuerpo varchar(2500), 
    respuesta varchar(2500), 
    fecha datetime NOT NULL,
    nif_cliente VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    id_producto int UNSIGNED NOT NULL, 
    CONSTRAINT pk_valoracion 
        PRIMARY KEY (id), 
    CONSTRAINT ak_valoracion 
        UNIQUE KEY (nif_cliente, id_producto), 
    CONSTRAINT fk_valoracion_cliente 
        FOREIGN KEY (nif_cliente) 
        REFERENCES cliente(nif)
        ON UPDATE CASCADE, 
    CONSTRAINT fk_valoracion_producto 
        FOREIGN KEY (id_producto) 
        REFERENCES producto(id), 
    CONSTRAINT ck_valoracion_calificacion 
        CHECK (calificacion BETWEEN 1 AND 5)
);

CREATE OR REPLACE TABLE tarjeta_bancaria ( -- Revisado
    numero varchar(256) NOT NULL, -- No necesita encriptación al no asociarse a un usuario (si NIF encriptado) - Clave primaria
    titular varchar(256) NOT NULL, -- No necesita encriptación al no asociarse a un usuario (si NIF encriptado)
    cvv varchar(3) NOT NULL, 
    fecha_caducidad date NOT NULL, 
    nif_cliente VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    CONSTRAINT pk_tarjeta 
        PRIMARY KEY (numero), 
    CONSTRAINT fk_tarjeta_cliente 
        FOREIGN KEY (nif_cliente) 
        REFERENCES cliente(nif)
        ON UPDATE CASCADE, 
    CONSTRAINT ck_tarjeta_cvv 
        CHECK (LENGTH(cvv) = 3)
);

CREATE OR REPLACE TABLE transporte ( -- Revisado
	nif varchar(9) NOT NULL,
	nombre varchar(50) NOT NULL,
	CONSTRAINT pk_transporte
		PRIMARY KEY (nif),
	CONSTRAINT ak_transporte
		UNIQUE KEY (nombre)
);

CREATE OR REPLACE TABLE pedido ( -- Revisado
    id int UNSIGNED NOT NULL AUTO_INCREMENT, 
    total decimal(10, 2) NOT NULL, 
    fecha_pedido datetime, 
    coste_envio decimal(10, 2), 
    tiempo_envio int, 
    nif_cliente VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    nif_transporte varchar(9), 
    id_dir_envio int UNSIGNED, 
    id_dir_fact int UNSIGNED, 
    num_tarjeta_bancaria varchar(256), -- Necesita encriptación (ver encriptación de tarjeta bancaria) - Se puede relacionar datos Cliente y Tarjeta
    CONSTRAINT pk_pedido 
        PRIMARY KEY (id), 
    CONSTRAINT fk_pedido_cliente 
        FOREIGN KEY (nif_cliente) 
        REFERENCES cliente(nif)
        ON UPDATE CASCADE, 
    CONSTRAINT fk_pedido_transporte 
        FOREIGN KEY (nif_transporte) 
        REFERENCES transporte(nif), 
    CONSTRAINT fk_pedido_direccion_envio 
        FOREIGN KEY (id_dir_envio) 
        REFERENCES direccion(id), 
    CONSTRAINT fk_pedido_direccion_fact 
        FOREIGN KEY (id_dir_fact) 
        REFERENCES direccion(id), 
    CONSTRAINT fk_pedido_tarjeta 
        FOREIGN KEY (num_tarjeta_bancaria) 
        REFERENCES tarjeta_bancaria(numero)
);

CREATE OR REPLACE TABLE linea_pedido ( -- Revisado
    id int NOT NULL, 
    cantidad int NOT NULL, 
    precio decimal(10, 2) NOT NULL, 
    base decimal(10, 2) NOT NULL, 
    iva decimal(10, 2) NOT NULL, 
    subtotal decimal(10, 2) NOT NULL, 
    estado enum('Cesta', 'Pendiente', 'Confirmado', 'Enviado', 'Entregado', 'Cancelado', 'En devolucion', 'Devuelto', 'Rechazado') NOT NULL, 
    fecha_envio datetime, 
    fecha_recepcion datetime, 
    id_producto int UNSIGNED NOT NULL, 
    id_pedido int UNSIGNED NOT NULL,
    CONSTRAINT pk_linea_pedido 
        PRIMARY KEY (id_pedido, id), 
    CONSTRAINT fk_linea_pedido_producto 
        FOREIGN KEY (id_producto) 
        REFERENCES producto(id), 
    CONSTRAINT fk_linea_pedido_pedido 
        FOREIGN KEY (id_pedido) 
        REFERENCES pedido(id)
);

CREATE OR REPLACE TABLE chat ( -- Revisado
    id int UNSIGNED NOT NULL AUTO_INCREMENT, 
    nif_usuario_1 VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    nif_usuario_2 VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    fecha_inicio datetime NOT NULL, 
    fecha_fin datetime, 
    CONSTRAINT pk_chat 
        PRIMARY KEY (id), 
    CONSTRAINT fk_chat_usuario_1 
        FOREIGN KEY (nif_usuario_1) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE, 
    CONSTRAINT fk_chat_usuario_2
        FOREIGN KEY (nif_usuario_2) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE
);

CREATE OR REPLACE TABLE mensaje ( -- Revisado
    id int UNSIGNED NOT NULL AUTO_INCREMENT, 
    id_chat int UNSIGNED NOT NULL, 
    nif_usuario VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    fecha_envio datetime NOT NULL, 
    contenido blob,
    CONSTRAINT pk_mensaje 
        PRIMARY KEY (id), 
    CONSTRAINT fk_mensaje_usuario 
        FOREIGN KEY (nif_usuario) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE, 
    CONSTRAINT fk_mensaje_chat
        FOREIGN KEY (id_chat) 
        REFERENCES chat(id)
);


CREATE OR REPLACE TABLE chat_archivado ( -- Revisado
    id int NOT NULL, 
    nif_usuario_1 VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    nif_usuario_2 VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    fecha_inicio datetime NOT NULL, 
    fecha_fin datetime, 
    CONSTRAINT pk_chat_archivado 
        PRIMARY KEY (id), 
    CONSTRAINT fk_chat_archivado_usuario_1 
        FOREIGN KEY (nif_usuario_1) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE, 
    CONSTRAINT fk_chat_archivado_usuario_2
        FOREIGN KEY (nif_usuario_2) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE
);

CREATE OR REPLACE TABLE mensaje_archivado ( -- Revisado
    id int NOT NULL, 
    id_chat int NOT NULL, 
    nif_usuario VARBINARY(255) NOT NULL, -- Encriptado AES habilitado
    fecha_envio datetime NOT NULL, 
    contenido blob,
    CONSTRAINT pk_mensaje_archivado 
        PRIMARY KEY (id), 
    CONSTRAINT fk_mensaje_archivado_usuario 
        FOREIGN KEY (nif_usuario) 
        REFERENCES usuario(nif) 
        ON UPDATE CASCADE, 
    CONSTRAINT fk_mensaje_archivado_chat
        FOREIGN KEY (id_chat) 
        REFERENCES chat_archivado(id)
);
set foreign_key_checks = 1;
