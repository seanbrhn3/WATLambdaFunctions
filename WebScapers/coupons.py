#https://www.dsw.com/en/us/brands/vans/N-1z14145?No=0
#row row-2cols--xs row-3cols--sm row-4cols--lg gutter
# from google_images_search import GoogleImagesSearch
from google_images_download import google_images_download
import boto3
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import os
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from selenium import webdriver
import time
urllib3.disable_warnings(InsecureRequestWarning)
import logging
class WATScrper():
    gfs = google_images_download.googleimagesdownload()
    client = boto3.client("s3")
    tile_class = None
    image_links = []
    link = None
    pool = urllib3.PoolManager()
    def __init__(self, link, tile_class):
        self.link = link
        self.tile_class = tile_class

    def scrape_shoes(self):
        #random headers to make website believe I'm a computer
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, "
            "like Gecko) Chrome/81.0.4044.141 Safari/537.36"
        }
        if self.link is not None:
            sneakerhead = requests.get(self.link,headers=headers)
        else:
            return "link is null"
        sneakerhead_object = BeautifulSoup(sneakerhead.content, "html.parser")
        #print(sneakerhead_object)
        #sneakerhead_image = sneakerhead_object.find_all("ul")
        sneakerhead_image = sneakerhead_object.find_all("section",{'class': self.tile_class})
        results = []
        for i in sneakerhead_image:
            data = i.find_all("a",{"class":"showPopup"})
            for val in data:
                results.append(val.attrs['data-url'])
        logging.info(f"Results: {results}")
        return results

def main():
    count = 0
    # Did not work
    # honey = WATScrper("https://www.joinhoney.com/search?q=sneakers","container-0-2-195")
    # honey.scrape_shoes()

    coupon_follow = WATScrper("https://couponfollow.com/site/sneakersnstuff.com#P428963","of")
    coupon_follow.scrape_shoes()

if __name__ in "__main__":
    main()
