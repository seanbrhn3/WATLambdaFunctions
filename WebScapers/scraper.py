from bs4 import BeautifulSoup
import requests
import os
from google_images_search import GoogleImagesSearch
import boto3
import time
import json

key_and_id = json.load(open("config.json", 'r'))
gfs = GoogleImagesSearch(key_and_id["key"], key_and_id["id"])
client = boto3.client("s3")

def scrape_shoes(link):
    sneakerhead = requests.get(link)
    sneakerhead_object = BeautifulSoup(sneakerhead.content, "html.parser")
    sneakerhead_image = sneakerhead_object.find_all("a", {"class": "product-item__title text--strong link"})
    # Create directory and add image
    if sneakerhead_image is None or len(sneakerhead_image) == 0:
        print("no images to collect")
    for image in sneakerhead_image:
        #send to s3
        print(image.text)
        dir = image.text
        client.put_object(Bucket="sagemakertestwat",Key=(dir))
        # Creates directory if exists
        if not os.path.exists("/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(image.text)):
            os.mkdir("/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(image.text))
        # adds image to directory
        shoe = image.text
        query(shoe)
        print("images collected")
#Creates folder for the image
def get_images(dir,shoe):
    name = dir.split("/")[1]
    for file in os.walk(dir):
        for i in file[2]:
            dir_name = file[0]+"/{}".format(i)
            with open(dir_name, 'rb') as data:
                client.upload_fileobj(data, "sagemakertestwat-dev", shoe+"/"+i)

#populates image folder with images
def query(name):
    file_types = ["png", "jpg"]
    img_size = [ 'imgSizeUndefined', 'HUGE', 'ICON', 'LARGE', 'MEDIUM', 'SMALL', 'XLARGE', 'XXLARGE']
    for size in img_size:
        for ftype in file_types:
            _search_params = {
                'q': name,
                'num': 10,
                'safe': 'active',
                'fileType': ftype,
                'imgType': 'photo',
                'imgSize': size,
                'print_urls': True
            }

            gfs.search(search_params=_search_params,
                       path_to_dir="/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(name))
            # for image in gfs.results():
            #     image.download("/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(name))
            #     image.resize(500, 500)
            get_images("~/soumtas_stuff/{}".format(name), name)
            time.sleep(10)

Links = ["https://www.sneakerhead.com/collections/shoes"]

num=1

for link in Links:
    scrape_shoes("https://www.sneakerhead.com/collections/shoes?page={}".format(num))
    num+=1
