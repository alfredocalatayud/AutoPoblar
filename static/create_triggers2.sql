CREATE TRIGGER IF NOT EXISTS usuario_bi_trigger
BEFORE INSERT ON usuario for each ROW 
BEGIN 
	SET new.fecha_alta = now();
END;

-- ooooooooooooooooooooooooooooooooooo

CREATE TRIGGER IF NOT EXISTS mensaje_bi_trigger
BEFORE INSERT ON mensaje for each ROW 
BEGIN 
	SET new.fecha_envio = now();
END;

-- ooooooooooooooooooooooooooooooooooo

CREATE TRIGGER IF NOT EXISTS chat_bi_trigger
BEFORE INSERT ON chat for each ROW 
BEGIN 
	SET new.fecha_inicio = now();
END;
