import sys
sys.path.append('../AutoPoblar')

import mysql.connector

from utiles import encriptar

# with open('./static/nifs.txt', 'rb') as input_file:
#     for i, line in enumerate(input_file):
#         # linea = line[:-1]
#         # print("{} {}".format(i, linea.encode('latin-1')))
#         # uncrypted_line = mi_desencripta(linea.encode('latin-1'))
#         # print(line[:-1])
#         decrypted_line = encriptar.mi_desencripta(line[:-2].replace(b'\\n', b'\n'))
#         print(decrypted_line)



#print(original)

db = mysql.connector.connect(
    host = "bbdd.dlsi.ua.es",
    user = "gi_acs128",
    passwd = "Caramelos1998",
    database = "gi_tierra_alicante"
)

mycursor = db.cursor()

mycursor.execute("SELECT distinct(nif_cliente) FROM valoracion;")

with open('./SQL/usuarios.sql', encoding="latin-1") as file:
            select = file.read().strip(';')
            print(select)
            mycursor.execute(select)

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