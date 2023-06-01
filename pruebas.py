import mysql.connector






# Import
import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


SALT = b'\x01\xaet\xd3&\xdb\xfb\x0b\x94f\xc2\xb2\xffm\xf0\x94\xf8K\xb4d\xef%\xf3\xcb\xb7\xaf\xcdH\x92\x81B\xa0' # Para encriptar la key generation
PASSWORD = "abcdefghijklmnopqrstuvwx"

def mi_encripta(line):
    key = PBKDF2(PASSWORD, SALT, dkLen=32)

    cipher = AES.new(key, AES.MODE_CBC)
    ciphered_data = cipher.encrypt(pad(line, AES.block_size))
    iv = cipher.iv

    return iv + ciphered_data

def mi_desencripta(encrypted_line):
    key = PBKDF2(PASSWORD, SALT, dkLen=32)

    iv = encrypted_line[:16]  # Los primeros 16 bytes son el IV
    ciphered_data = encrypted_line[16:]  # El resto de los bytes son los datos encriptados

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphered_data)

    # Elimina el relleno (padding) de los datos desencriptados
    decrypted_data = unpad(decrypted_data, AES.block_size)

    return decrypted_data.decode()

def decrypt_line(encrypted_line, password):
    backend = default_backend()

    key = password
    iv = os.urandom(16) # Convertir la representación hexadecimal del IV en bytes

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(bytes.fromhex(encrypted_line[32:])) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data.decode()

linea_encriptada = mi_encripta(b"Hola")

print(mi_desencripta(linea_encriptada))


#print(original)

# db = mysql.connector.connect(
#     host = "bbdd.dlsi.ua.es",
#     user = "gi_acs128",
#     passwd = "Caramelos1998",
#     database = "gi_tierra_alicante"
# )

# mycursor = db.cursor()

# mycursor.execute("SELECT distinct(nif_cliente) FROM valoracion;")

# for i in mycursor:
#     print(i[0])

# salt = b'\x01\xaet\xd3&\xdb\xfb\x0b\x94f\xc2\xb2\xffm\xf0\x94\xf8K\xb4d\xef%\xf3\xcb\xb7\xaf\xcdH\x92\x81B\xa0' # Para encriptar la key generation
# password = "abcdefghijklmnopqrstuvwx"

# key = PBKDF2(password, salt, dkLen=32)

# message = b"Hola"

# cipher = AES.new(key, AES.MODE_CBC)
# ciphered_data = cipher.encrypt(pad(message, AES.block_size)) 

# with open('encrypted.bin', 'wb') as f:
#     f.write(cipher.iv)
#     f.write(ciphered_data)

# with open('encrypted.bin', 'rb') as f:
#     iv = f.read(16)
#     decrypt_data = f.read()

# cipher = AES.new(key, AES.MODE_CBC, iv = iv)
# original = unpad(cipher.decrypt(decrypt_data), AES.block_size)

# with open('key.bin', 'wb') as f:
#     f.write(key)