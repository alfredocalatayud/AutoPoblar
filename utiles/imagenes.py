# import requests
# from googletrans import Translator

# class UnsplashImageDownloader:
#     def __init__(self, query):
#         self.querystring = {"query": f"{query}", "per_page": "1"}
#         self.headers = {"cookie": "ugid=aacdcdf3a2acebee349c2e196e621b975571725"}
#         self.url = "https://unsplash.com/napi/search/photos"

#         self.query = query

#     def get_total_images(self):
#         with requests.request("GET", self.url, headers=self.headers, params=self.querystring) as rs:
#             json_data = rs.json()

#         return json_data["total"]

#     def get_links(self, pages_, quality_):
#         all_links = []
#         for page in range(1, int(pages_) + 1):
#             self.querystring["page"] = f"{page}"

#             response = requests.request("GET", self.url, headers=self.headers, params=self.querystring)
#             response_json = response.json()
#             all_data = response_json["results"]

#             for data in all_data:
#                 name = None
#                 try:
#                     name = data["sponsorship"]["tagline"]
#                 except:
#                     pass
#                 if not name:
#                     try:
#                         name = data['alt_description']
#                     except:
#                         pass
#                 if not name:
#                     name = data['description']
#                 try:
#                     image_urls = data["urls"]
#                     required_link = image_urls[quality_]
#                     all_links.append(required_link)
#                 except:
#                     pass

#         return all_links


# def url_imagen(categoria):
#     translator = Translator()
#     categoria_en = translator.translate(categoria, dest='en').text

#     search = categoria_en

#     unsplash = UnsplashImageDownloader(search)

#     total_image = unsplash.get_total_images()

#     if total_image == 0:
#         print(categoria_en)
#         print("sorry, no image available for this search")
#         exit()

#     number_of_images = 1

#     pages = float(number_of_images / 20)
#     if pages != int(pages):
#         pages = int(pages) + 1

#     quality = 'full'
#     image_links = unsplash.get_links(pages, quality)

#     return image_links[0]