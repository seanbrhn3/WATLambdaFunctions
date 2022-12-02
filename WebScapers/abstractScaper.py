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


class WATScrper():
    key_and_id = json.load(open("config.json", 'r'))
    # gfs = GoogleImagesSearch(key_and_id["key"], key_and_id["id"])
    gfs = google_images_download.googleimagesdownload()
    client = boto3.client("s3")
    tile_class = None
    image_links = []
    link = None

    def __init__(self, link, tile_class):
        self.link = link
        self.tile_class = tile_class

    def scrape_shoes(self):
        if self.link is not None:
            sneakerhead = requests.get(self.link)
        else:
            return "link is null"
        sneakerhead_object = BeautifulSoup(sneakerhead.content, "html.parser")
        sneakerhead_image = sneakerhead_object.find_all("a", {"class": self.tile_class})
        print(sneakerhead_image)
        for i in sneakerhead_image:
            fond = i.find("div",
                          {"class": self.tile_class})
            print("heres what was found", fond)
            self.image_links.append(fond.text)
        for image in self.image_links:
            image = image.rstrip("\n")
            self.client.put_object(Bucket="sagemakertestwat-dev", Key=(image))
            # adds image to directory
            shoe = image
            self.download_google_staticimages(shoe)
            print("images collected")

    # Creates folder for the image
    def get_images(self, dir):
        for file in os.walk(dir):
            for i in file[2]:
                print("not sure what file[2] is so ", i)
                if ".jpg" in i:
                    os.system("mv {} ~/PycharmProjects/WATWS/shoes/{}".format(dir))
                    # with open(name, 'rb') as data:
                    #     client.upload_fileobj(data, "sagemakertestwat-dev", name+"/"+i)

    # populates image folder with images

    """
    function name: download_google_staticimage,
    purpose: use the google_images_download library to download the she image passed in the scrape shoes function.
    This image is downloaded from goole and put in the downloads directory. I call get_images to put the image in 
    in the shoe directory for the machine learning  algo, and then send the images into the  dev/prod s3 bucket
    """

    def download_google_staticimages(self, name):
        searchurl = 'https://www.google.com/search?q=' + name + '&source=lnms&tbm=isch'
        dirs = name.rstrip("\n")
        maxcount = 1000
        print("Grabbing images for {}".format(dirs))
        chromedriver = "/Users/seanbrown/PycharmProjects/WATWS/chromedriver"

        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        # options.add_argument('--headless')
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

        # elements = browser.find_elements_by_xpath('//div[@id="islrg"]')
        # page_source = elements[0].get_attribute('innerHTML')
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
                os.system("sudo chmod 777 {}".format(path))
                os.system("touch {}/{}.jpg".format(path, dirs))
                with open(path + "/{}".format(dirs + str(count) + ".jpg"), 'wb') as f:
                    f.write(rawdata)
                print("shoe {}".format(count))
                # get_images(name)
                # os.system("cp {} ~/PycharmProjects/WATWS/shoes/{}".format(dirs))
                with open(path + "/{}".format(dirs + str(count) + ".jpg"), 'rb') as data:
                    boto3.client.upload_fileobj(data, "sagemakertestwat-dev", os.path.join(dirs, '.jpg'))
                print("Able to grab {}".format(count))
                count += 1
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
    Just create a WATScraper object and run it
"""


def main():
    Links = ["https://www.asics.com/us/en-us/men/c/aa10000000/"]
    num = 1
    go = False
    balenciaga = WATScrper("https://www.balenciaga.com/us/men/shoes", "item-display-image-container item-link")
    louive = WATScrper("https://us.louisvuitton.com/eng-us/men/shoes/all-shoes/_/N-1uxy4tc",
                       "lv-smart-link lv-product-card -compact-large")
    louive_women = WATScrper("https://us.louisvuitton.com/eng-us/women/shoes/all-shoes/_/N-r3oj04",
                             "lv-smart-link lv-product-card -compact-large")
    asics = WATScrper("https://www.asics.com/us/en-us/men/c/aa10000000/", "product-tile__link js-product-tile")
    balenciaga.scrape_shoes()
    louive.scrape_shoes()
    louive_women()
    asics.scrape_shoes()
    # while True:
    #     start= 26
    #     if go == False:
    #         gp = True
    #         asics = WATScrper("https://www.asics.com/us/en-us/men/c/aa10000000/", "product-tile__link js-product-tile")
    #     else:
    #         start = start * 2
    #         grab_link = "https://www.asics.com/us/en-us/men/c/aa10000000/?start={}".format(start)
    #         asics.scrape_shoes("https://www.asics.com/us/en-us/men/c/aa10000000/?start={}".format(start))


if __name__ in "__main__":
    main()
