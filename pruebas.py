import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import requests
import io

PATH = "C:\\Users\\alfre\\Desktop\\Alfredo JR\\AutoPoblar\\utiles\\chromedriver.exe"

# wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

search_url = "https://www.google.es/search?q={}&client=img&source=Inms&tbm=isch"

# wd.get(search_url.format("paella+valenciana"))

def init_driver():
    options = webdriver.FirefoxOptions()

    # Maximized
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')

    driver = webdriver.Firefox(options=options)

    return driver


def get_images_from_google(wd, delay, max_images):
    url = search_url.format("paella")

    wd.get(url)

    # cookie = wd.find_elements(By.CLASS_NAME, "VfPpkd-vQzf8d")
    # time.sleep(5)
    wd.find_element(By.XPATH, "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span").click()
    print("hola")


    image_urls = set()

    wd.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img").click()
    xpath = "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[{}]/a[1]/div[1]/img"
    # /html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[1]/a[1]/div[1]/img
    # /html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[2]/a[1]/div[1]/img
    # /html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[3]/a[1]/div[1]/img

    i = 1
    while len(image_urls) <= 0:
        if i % 25 == 0:
            continue 
        
        n_xpath = xpath.format(i)
        wd.find_element(By.XPATH, n_xpath).click()

        if i == 5:
            break
        i += 1

    # print(image.get_attribute('src'))

    # while len(image_urls) < max_images:
    #     thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

    #     for img in thumbnails[len(image_urls): max_images]:
    #         try:
    #             img.click()
    #             time.sleep(delay)
    #         except:
    #             continue
    #         images = wd.find_elements(By.CLASS_NAME, "r48jcc pT0Scc iPVvYb")
    #         for image in images:
    #             print("hola")
    #             if image.get_attribute('src') and 'http' in image.get_attribute('src'):
    #                 image_urls.add(image.get_attribute('src'))
    #                 continue
    # return image_urls

wd = init_driver()
get_images_from_google(wd, 5, 1)
