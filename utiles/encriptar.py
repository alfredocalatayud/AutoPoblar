import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

SALT = b' a=\x98^(\xaa\xe5\xd2.g\xaen\x8d/8'
PASSWORD = "abcdefghijklmnopqrstuvwx"

def mi_encripta(line):
    key = PBKDF2(PASSWORD.encode(), SALT, dkLen=32)

    cipher = Cipher(algorithms.AES(key), modes.CBC(SALT), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    padded_data = padder.update(line) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return encrypted_data

def mi_desencripta(encrypted_line):
    key = PBKDF2(PASSWORD.encode(), SALT, dkLen=32)

    cipher = Cipher(algorithms.AES(key), modes.CBC(SALT), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    decrypted_data = decryptor.update(encrypted_line) + decryptor.finalize()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data.decode()