import bcrypt

def mi_encripta(line):
    pwd = line
    salt = bcrypt.gensalt()
    contrasenya = bcrypt.hashpw(pwd.encode(), salt)

    return contrasenya.decode('utf-8')