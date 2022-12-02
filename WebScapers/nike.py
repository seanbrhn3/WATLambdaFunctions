
# from google_images_search import GoogleImagesSearch
from google_images_download import google_images_download
import boto3
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import shutil
import json
import os
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from selenium import webdriver
import logging 
import time

urllib3.disable_warnings(InsecureRequestWarning)

"""
THINGS TO DO:
    1. Make sure the images data is being fully downloaded with no  erros.
    2. Delete all files after they go to s3
    3. Make sure this works for all scrapers
    4. Images have zero bytes. Check line 172; may need to get rid of verify
        Stream is their to keep the connection alive throughout  the download process
"""
"""
This class mainly focuses on extracting all title from images. 
This has the assumption that the website puts the name of the shoe 
in the title. That may not be the case for some websites. Proceed accordingly

Website that use titles within images:
balenciaga

"""

class WATScrper():
    key_and_id = json.load(open("config.json", 'r'))
    # gfs = GoogleImagesSearch(key_and_id["key"], key_and_id["id"])
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
            print("here", self.link)
            sneakerhead = requests.get(self.link,headers=headers)
        else:
            return "link is null"
        sneakerhead_object = BeautifulSoup(sneakerhead.content, "html.parser")
        logging.info(f"LOOO HERE {sneakerhead_object}")
        sneakerhead_image = sneakerhead_object.find_all("span")
        sneakerhead_image = sneakerhead_object.find("div",{'class':self.tile_class})
        for i in sneakerhead_image:
            print(i.text)
            # found_title = i.find("div",
            #               {"class": self.tile_class})
            found =i.text.replace("$","")
            logging.info("here's what was found", found)
            self.image_links.append(found)

            self.client.put_object(Bucket="sagemakertestwat-dev", Key=(found))
            # adds image to directory
            self.download_google_staticimages(found)
            print("images collected")

    # Creates folder for the image
    def get_images(self, dir):
        for file in os.walk(dir):
            for i in file[2]:
                print("not sure what file[2] is so ", i)
                if ".jpg" in i:
                    os.system("mv {} ~/PycharmProjects/WATWS/shoes/{}".format(dir))
    # populates image folder with images

    """
    function name: download_google_staticimage,
    purpose: use the google_images_download library to download the she image passed in the scrape shoes function.
    This image is downloaded from goole and put in the downloads directory. I call get_images to put the image in 
    in the shoe directory for the machine learning  algo, and then send the images into the  dev/prod s3 bucket
    """

    def download_google_staticimages(self, name):
        searchurl = 'https://www.google.com/search?q=' + name + '&source=lnms&tbm=isch'
        dirs = name
        maxcount = 1000
        print("Grabbing images for {}".format(dirs))
        chromedriver ="/usr/local/bin/chromedriver"

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')

        browser = webdriver.Chrome(chromedriver, options=options)


        browser.set_window_size(1280, 1024)
        browser.get(searchurl)
        time.sleep(1)

        print(f'Getting you a lot of images. This may take a few moments...')

        element = browser.find_element_by_tag_name('body')

        # Scroll down
        # for i in range(30):
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

        try:
            browser.find_element_by_id('smb').click()
            for i in range(50):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)
        except:
            for i in range(10):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)

        print(f'Reached end of page.')
        time.sleep(0.5)
        print(f'Retry')
        time.sleep(0.5)

        # Below is in japanese "show more result" sentences. Change this word to your lanaguage if you require.
        try:
            browser.find_element_by_xpath('//input[@value="Show more result"]').click()
        except:
            print("We've reached the end of the page...")

        # Scroll down 2
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

        try:
            browser.find_element_by_id('smb').click()
            for i in range(50):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)
        except:
            for i in range(10):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)
        page_source = browser.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        images = soup.find_all('img')

        urls = []
        for image in images:
            url = image.get('data-src',"src")
            if "https://" in url:
                urls.append(url)
        count = 0
        if urls:
            for url in urls:
                # try:

                #res = requests.get(url)
                res = self.pool.request('GET',url)
                # res.raw.decode_content  = True # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                # rawdata = res.raw.read()
                dirs = dirs.rstrip().split("\n")
                print("MUST LOOK HEREEEEEEEEEEE",dirs)
                dirs = dirs[0]
                replace = ["."," "]
                for i in dirs:
                    if i in replace:
                        dirs = dirs.replace(i,"_")
                dirs = dirs.replace(i, "_")
                filename = dirs+str(count)+".jpg"
                #Make directory
                try:
                    with open(filename, 'wb') as f:
                        f.write(res.data)
                        #shutil.copyfileobj(res.raw, f)
                    with open(filename, 'rb') as f:
                        self.client.upload_fileobj(f, "sagemakertestwat-dev", dirs+"/"+filename)
                    os.remove(filename)
                except:
                    print("could not upload")
                print("shoe {}".format(count))
                print("Able to grab {}".format(count))
                count += 1

        browser.close()
        return count


# Main block
"""
    Just create a WATScraper object and run it
"""


def main():
    # new_releases = WATScrper("https://www.nike.com/w/new-mens-shoes-3n82yznik1zy7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")
    # new_releases.scrape_shoes()
    # nike_kids = WATScrper("https://www.nike.com/w/boys-shoes-1onrazy7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")
    # nike_kids.scrape_shoes()
    # nike_women = WATScrper("https://www.nike.com/w/womens-shoes-5e1x6zy7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")
    # nike_women.scrape_shoes()
    # nike = WATScrper("https://www.nike.com/w/mens-shoes-nik1zy7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")
    # nike.scrape_shoes()

    jordans = WATScrper("https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")

    bunches = WATScrper("https://www.nike.com/w/shoes-y7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")

    #jordans.scrape_shoes()
    bunches.scrape_shoes()
if __name__ in "__main__":
    main()
