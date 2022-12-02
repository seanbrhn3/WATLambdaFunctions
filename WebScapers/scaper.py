from bs4 import BeautifulSoup
import requests
import os
from google_images_search import GoogleImagesSearch
import boto3
import time
import schedule

gfs = GoogleImagesSearch("AIzaSyDPG9EHvrKmhdkUJfzZggbBWbYZIrkvs1I", "003396785806028555923:uakgw7rdnzd")
client = boto3.client("s3")

def scrape_shoes(link):
    nike = requests.get(link)
    nike_shoes = BeautifulSoup(nike.content, "html.parser")
    nike_images = nike_shoes.find_all("div", {"class": "product-card__body"})

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
            }
            print(name,size)
            # gfs.search(search_params=_search_params,
            #            path_to_dir="/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(name))
            for image in gfs.results():
                image.download("/Users/seanbrown/PycharmProjects/ShoeScraper/shoes/{}".format(name))
                image.resize(500, 500)
            get_images("~/soumtas_stuff/{}".format(name), name)
            time.sleep(10)

Links = ["https://store.nike.com/us/en_us/pw/mens-shoes/7puZoi3?ipp=120", "https://www.nike.com/w/mens-shoes-nik1zy7ok",
         "https://www.nike.com/w/mens-training-gym-shoes-58jtoznik1zy7ok",
         "https://www.nike.com/w/mens-lifestyle-shoes-13jrmznik1zy7ok",
         "https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok",
         "https://www.nike.com/w/mens-running-shoes-37v7jznik1zy7ok",
         "https://www.nike.com/w/mens-basketball-shoes-3glsmznik1zy7ok",
         "https://www.nike.com/w/mens-training-gym-shoes-58jtoznik1zy7ok",
         "https://www.nike.com/w/mens-soccer-shoes-1gdj0znik1zy7ok",
         "https://www.nike.com/w/mens-skateboarding-shoes-8mfrfznik1zy7ok",
         "https://www.nike.com/w/mens-football-shoes-3hj8mznik1zy7ok",
         "https://www.nike.com/w/mens-baseball-shoes-99fchznik1zy7ok",
         "https://www.nike.com/w/mens-golf-shoes-23q9wznik1zy7ok",
         "https://www.nike.com/w/mens-tennis-shoes-ed1qznik1zy7ok",
         "https://www.nike.com/w/mens-track-field-shoes-7nem3znik1zy7ok"]

# for link in Links:
#     scrape_shoes(link)

