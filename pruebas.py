import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import io
import mysql.connector

import bcrypt

# wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

search_url = "https://www.google.es/search?q={}&client=img&source=Inms&tbm=isch"

# wd.get(search_url.format("paella+valenciana"))


pwd = '1234'
salt = bcrypt.gensalt()
contrasenya = bcrypt.hashpw(pwd.encode(), salt)

conn = mysql.connector.connect(host='bbdd.dlsi.ua.es', user='gi_acs128', passwd='Caramelos1998', database='gi_acs128')
cursor = conn.cursor()

query = "UPDATE usuario \
         SET contrasenya = \"{}\" \
         WHERE aes_decrypt(nif, SHA2('abcdefghijklmnopqrstuvwx', 512)) = '14959459Q';".format(contrasenya.decode('utf-8'))


print(query)

cursor.execute(query)
cursor.execute("commit")

