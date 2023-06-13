import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
import io


search_url = "https://www.google.es/search?q={}&client=img&source=Inms&tbm=isch"


def init_driver():
    options = webdriver.FirefoxOptions()

    # Maximized
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')

    # Minimized
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')

    driver = webdriver.Firefox(options=options)

    return driver


def get_images_from_google(wd, delay, max_images, contenido):
    url = search_url.format(contenido)

    wd.get(url)

    # time.sleep(5)
    try:
        wd.find_element(By.XPATH, "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span").click()
    except:
        pass


    image_urls = set()

    wd.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img").click()
    xpath = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div[1]/div/div[1]/div[1]/span/div[1]/div[1]/div[{}]/a[1]/div[1]/img"

    i = 1
    while len(image_urls) < max_images:
        if i % 25 == 0:
            break 
        
        n_xpath = xpath.format(i)
        wd.find_element(By.XPATH, n_xpath).click()

        time.sleep(0.5)

        try:
            imagen = wd.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]")
            source = imagen.get_attribute('src')

            if 'http' in source:
                return source
        except:
            i += 1
            continue
        

