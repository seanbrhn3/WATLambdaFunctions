from builtins import dir
from bs4 import BeautifulSoup
import requests
import os
#from google_images_search import GoogleImagesSearch
from google_images_download import google_images_download
import boto3
import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import shutil
import json
import os
import argparse
import sys
import requests
import urllib
import urllib3
from urllib3.exceptions import InsecureRequestWarning

import datetime
import time

key_and_id = json.load(open("config.json", 'r'))
#gfs = GoogleImagesSearch(key_and_id["key"], key_and_id["id"])
gfs = google_images_download.googleimagesdownload()
client = boto3.client("s3")
urllib3.disable_warnings(InsecureRequestWarning)
image_links = []

def scrape_shoes(link):
    sneakerhead = requests.get(link)
    sneakerhead_object = BeautifulSoup(sneakerhead.content, "html.parser")
    sneakerhead_image = sneakerhead_object.find_all("a",{"class":"product-tile__link js-product-tile"})
    for i in sneakerhead_image:
        fond = i.find("div",{"class":"product-tile__text product-tile__text--large product-tile__text--underline"})
        image_links.append(fond.text)
    for image in image_links:
        image = image.rstrip("\n")
        client.put_object(Bucket="sagemakertestwat-dev", Key=(image))
        # adds image to directory
        shoe = image
        download_google_staticimages(shoe)
        print("images collected")

#Creates folder for the image
def get_images(dir):
    for file in os.walk(dir):
        for i in file[2]:
            print("not sure what file[2] is so ", i)
            if ".jpg" in i:
                os.system("mv {} ~/PycharmProjects/WATWS/shoes/{}".format(dir))
                # with open(name, 'rb') as data:
                #     client.upload_fileobj(data, "sagemakertestwat-dev", name+"/"+i)

#populates image folder with images

"""
function name: download_google_staticimage,
purpose: use the google_images_download library to download the she image passed in the scrape shoes function.
This image is downloaded from goole and put in the downloads directory. I call get_images to put the image in 
in the shoe directory for the machine learning  algo, and then send the images into the  dev/prod s3 bucket
"""
def download_google_staticimages(name):
    searchurl = 'https://www.google.com/search?q=' + name + '&source=lnms&tbm=isch'
    dirs = name.rstrip("\n")
    maxcount = 1000
    print("Grabbing images for {}".format(dirs))
    chromedriver = "/usr/local/bin/chromedriver"

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    #options.add_argument('--headless')
    browser = webdriver.Chrome(chromedriver, options=options)
    # try:
    #     browser = webdriver.Chrome(chromedriver, options=options)
    # except Exception as e:
    #     print(f'No found chromedriver in this environment.')
    #     print(f'Install on your machine. exception: {e}')
    #     sys.exit()

    browser.set_window_size(1280, 1024)
    browser.get(searchurl)
    time.sleep(1)

    print(f'Getting you a lot of images. This may take a few moments...')

    element = browser.find_element_by_tag_name('body')

    # Scroll down
    #for i in range(30):
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

    #elements = browser.find_elements_by_xpath('//div[@id="islrg"]')
    #page_source = elements[0].get_attribute('innerHTML')
    page_source = browser.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    images = soup.find_all('img')

    urls = []
    for image in images:
        try:
            url = image['data-src']
            if not url.find('https://'):
                urls.append(url)
        except:
            try:
                url = image['src']
                if not url.find('https://'):
                    urls.append(image['src'])
            except Exception as e:
                print(f'No found image sources.')
                print(e)

    count = 0
    if urls:
        for url in urls:
            # try:
            res = requests.get(url, verify=False, stream=True)
            rawdata = res.raw.read()
            # os.system("sudo mkdir ~/PycharmProjects/WATWS/shoes/{}".format(name))
            # if os.path.exists("~/PycharmProjects/WATWS/shoes/{}".format(name)):
            dirs = dirs.rstrip().split("\n")
            dirs = dirs[1]
            path = os.path.join("/shoes", dirs)
            if not os.path.exists(path):
                os.mkdir(path)
            print("path bieng used",path)
            os.system("sudo chmod 777 {}".format(path))
            the_shoe_image  = "{}/{}.jpg".format(path,dirs)
            os.system("sudo chmod 777 {}".format(the_shoe_image))
            try:
                with open(the_shoe_image, 'wb') as f:
                    f.write(rawdata)
                count = count + 1
                print("shoe {}".format(count))
                # get_images(name)
                # os.system("cp {} ~/PycharmProjects/WATWS/shoes/{}".format(dirs))
                with open(the_shoe_image, 'rb') as data:
                    client.upload_fileobj(data, "sagemakertestwat-dev", os.path.join(dirs, '.jpg'))
                print("Able to grab {}".format(count))
                count += 1
            except:
                print("unable to get image")
            break
                # else:
                #     print("path does not exist")
            # except Exception as e:
            #     print('Failed to write rawdata.')
            #     print(e)

    browser.close()
    return count

# Main block
"""
Main function taking in links and extracting all of the names to get images
"""
def main():
    Links = ["https://www.asics.com/us/en-us/men/c/aa10000000/"]
    num=1
    go = False

    while True:
        start= 26
        if go == False:
            gp = True
            scrape_shoes("https://www.asics.com/us/en-us/men/c/aa10000000/")
        else:
            start = start * 2
            scrape_shoes("https://www.asics.com/us/en-us/men/c/aa10000000/?start={}".format(start))


if __name__ in "__main__":
    main()
