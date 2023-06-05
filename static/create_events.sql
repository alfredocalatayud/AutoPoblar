CREATE EVENT IF NOT EXISTS archivar_chats
	ON SCHEDULE EVERY 1 WEEK
	STARTS CURRENT_TIMESTAMP
	DO
		BEGIN
			START TRANSACTION;
				INSERT INTO chat_archivado SELECT * 
					FROM chat
					WHERE chat.fecha_fin IS NOT NULL;
				INSERT INTO mensaje_archivado SELECT * 
					FROM mensaje 
					WHERE mensaje.id_chat IN (SELECT chat.id FROM chat WHERE chat.fecha_fin IS NOT NULL);
				DELETE FROM mensaje 
					WHERE mensaje.id_chat IN (SELECT chat.id FROM chat WHERE chat.fecha_fin IS NOT NULL);
				DELETE FROM chat
					WHERE chat.fecha_fin IS NOT NULL;
			COMMIT;
		END;
		
CREATE EVENT IF NOT EXISTS actualizar_relevancia_productos
	ON SCHEDULE EVERY 1 WEEK
	STARTS CURRENT_TIMESTAMP
	DO
		BEGIN
			UPDATE producto SET relevancia = (SELECT calcular_relevancia(id));
		END;
		
CREATE EVENT IF NOT EXISTS desactivar_productos_no_vendidos
	ON SCHEDULE EVERY 1 WEEK
	STARTS CURRENT_TIMESTAMP
	DO
		BEGIN
			UPDATE producto p
				SET p.activo = 0
				WHERE NOT EXISTS (
    				SELECT 1
    				FROM linea_pedido lp
    				INNER JOIN pedido pe ON lp.id_pedido = pe.id
    				WHERE lp.id_producto = p.id
    				AND pe.fecha_pedido >= (now() - INTERVAL 1 MONTH)
				) 
				AND (SELECT COUNT(*) FROM linea_pedido lp WHERE lp.id_producto = p.id) > 0;
		END;
		