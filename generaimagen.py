"""
    image downloader from unsplash website
"""

import requests
from bs4 import BeautifulSoup
import threading
import os
import shutil
import time


def get_links(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.content, "html.parser")

    links_list = {}

    image_tags = soup.select('figure div.YdIix div.L34o8 div.zmDAx a div.MorZF img')

    for tags in image_tags:
        data = tags.attrs['srcset']
        datas = data.split(',')

        for data in datas:

            image_link = data.split(" ")

            resolution_index = 1
            link_index = 0

            if len(image_link) == 3:
                image_link.pop(0)
            print("----------- ", image_link)

            if not links_list.get(image_link[resolution_index]):
                links_list[image_link[resolution_index]] = []
            links_list[image_link[resolution_index]].append(image_link[link_index])
    return links_list


def download_image(link, index):
    with requests.get(link) as r:
        with open(f"{FOLDER}/image{index}.jpg", "wb") as f:
            f.write(r.content)
        print(f"image-{index} downloaded")


def initialise_threads(urls):
    index = 1
    for link in urls:
        t = threading.Thread(target=download_image, args=(link,index,))
        index += 1
        threads.append(t)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def download(urls):
    initialise_threads(urls)


if __name__ == '__main__':
    FOLDER = "unsplash"
    if os.path.exists(FOLDER):
        shutil.rmtree(FOLDER)

    os.mkdir(FOLDER)

    base_url = "https://unsplash.com/s/photos/"

    threads = []

    print("This is a script to download image from unsplash website.\n")
    search = input("What do you want to search for ? ")

    search_url = base_url + '-'.join(search.split(' '))

    start = time.time()
    print("fetching the links...........")
    links = get_links(search_url)

    count = 0
    for links_list in links.values():
        count += len(links_list)

    print(f"\n{count} links fetched.\ntime took : {time.time() - start}\n")

    print("Available resolutions : ")
    for resolution in links:
        print(resolution)

    resolution = input("Enter width : ")

    required_urls = links[f"{resolution}w"]
    quantity = int(input(f"There are {len(required_urls)} images. How many do you want to download ? "))
    required_urls = required_urls[:quantity]

    start = time.time()
    print("\ndownload started........\n")
    download(required_urls)
    print('\n{} images downloaded\ntime took {:.2f}'.format(len(required_urls), time.time()-start))


