from bs4 import BeautifulSoup
import requests
import os
from google_images_search import GoogleImagesSearch
import boto3
import time
import schedule
import wget
import shutil
gfs = GoogleImagesSearch("AIzaSyDPG9EHvrKmhdkUJfzZggbBWbYZIrkvs1I", "003396785806028555923:uakgw7rdnzd")
client = boto3.client("s3")

def scrape_shoes(link):
    nike = requests.get(link)
    nike_shoes = BeautifulSoup(nike.content, "html.parser")
    nike_images = nike_shoes.find("a", {"class": "lv-smart-link lv-product-card -compact-large"})
    print(nike_images)
    # Create directory and add image
    for image in nike_images:
        #send to s3
        dir = image.figure.a.text+"/"
        client.put_object(Bucket="sagemakertestwat",Key=(dir))
        # Creates directory if exists
        if not os.path.exists("/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(image.figure.a.text)):
            os.mkdir("/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(image.figure.a.text))
        # adds image to directory
        shoe = image.figure.a.text
        query(shoe)
        print("images collected")

def get_images(dir,shoe):
    name = dir.split("/")[1]
    for file in os.walk(dir):
        for i in file[2]:
            dir_name = file[0]+"/{}".format(i)
            with open(dir_name, 'rb') as data:
                client.upload_fileobj(data, "sagemakertestwat", shoe+"/"+i)
            #client.upload_file(dir_name,"sagemakertestwat",name+"/"+i)

def query(name):
    file_types = ["png", "jpg"]
    img_size = [ "large", "xlarge", "xxlarge", "medium", "icon", "huge"]
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
            print(name,size)
            gfs.search(search_params=_search_params,
                       path_to_dir="/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(name))
            # for image in gfs.results():
            #     image.download("/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(name))
            #     image.resize(500, 500)
            get_images("~/soumtas_stuff/{}".format(name), name)
            time.sleep(10)

Links = ["https://us.louisvuitton.com/eng-us/men/shoes/all-shoes/_/N-1uxy4tc"]

for link in Links:
    scrape_shoes(link)

