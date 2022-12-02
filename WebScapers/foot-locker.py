# from google_images_search import GoogleImagesSearch
import glob

from google_images_download import google_images_download
import boto3
from bs4 import BeautifulSoup
import shutil
import json
import os
import requests
import urllib3
from selenium.webdriver.common.by import By
from urllib3.exceptions import InsecureRequestWarning
import selenium  # Using selenium 4. There have been many changes from version 3
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
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


class WATScrper:
    # gfs = GoogleImagesSearch(key_and_id["key"], key_and_id["id"])
    gfs = google_images_download.googleimagesdownload()
    client = boto3.client("s3")
    tile_class = None
    image_links = []
    link = None
    pool = urllib3.PoolManager()

    def __init__(self, link, tile_class, element=None):
        self.link = link
        self.element = element
        self.tile_class = tile_class

    def scrape_shoes(self):
        button = True
            # try:
        browser = self.enable_browser()
        browser.get(self.link)
        time.sleep(5)
        browser.refresh()
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        # spans = browser.find_elements(By.CLASS_NAME,"sc-ehMyHa.dPMWge") These are the next and buttons
        element = browser.find_elements(By.CLASS_NAME, self.tile_class)
        link = browser.find_element(By.CLASS_NAME, "Link")
        browser.execute_script("arguments[0].click();", link)
        #link.click()
        for i in element:
            print(i.text)
            self.download_google_staticimages(i.text)

        return

    def enable_browser(self):
        options = selenium.webdriver.ChromeOptions()
        prefs = {"download.default_directory": "/tmp/"}
        #options.add_argument('--headless')  # Chrome will operate in the background and won't open a windowc
        # options.add_experimental_option("prefs", prefs)  # This changes the download.default_directory to /tmp/
        # options.add_experimental_option("detach", True)
        browser = selenium.webdriver.Chrome(service=Service(ChromeDriverManager(path="/tmp/").install()),
                                            options=options)
        return browser

    def find_next_button(self, buttons):
        for button in buttons:
            next_text = button.text
            if 'Next' in next_text:
                print("[+] Next page found")
                return button
        return "Unable to find next page"

    def get_names(self, elements):
        print("[+] Collecting all shoes")
        names = []
        for element in elements:
            images = element.find_elements(By.TAG_NAME, "img")
            if len(images) > 0:
                for img in images:
                    name = img.get_attribute("alt")
                    name = name.replace(" ", "-")
                    name = name.replace("'", "")
                    names.append(name)
        print(f"[+] Shoes Collected! {len(names)}")
        return names

    def download_google_staticimages(self, dirs):
        dirs = dirs.replace(" ", "-")
        if "(" in dirs or ")" in dirs:
            dirs = dirs.replace("(","")
            dirs = dirs.replace(")", "")
        search_url = "https://www.google.com/search?q=" + dirs + "&source=lnms&tbm=isch"
        print(f"Grabbing images for {dirs}")
        browser = self.enable_browser()
        browser.get(search_url)
        time.sleep(1)
        print(f'Getting you  a lot of images. This may take a few moments...')
        print(f"{search_url}")
        element = browser.find_element(By.ID, 'yDmH0d')
        # Scroll down
        # for i in range(30):
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

        try:
            browser.find_element(By.ID, 'smb').click()
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
            browser.find_element(By.XPATH, '//input[@value="Show more result"]').click()
        except:
            print("We've reached the end of the page...")

        count = 0
        # Scroll down 2
        while count <= 100:
            for i in range(50):
                element.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.3)

            try:
                browser.find_element(By.ID, 'smb').click()
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
                url = image.get('data-src', "src")
                if "https://" in url:
                    urls.append(url)
            if urls:
                for url in urls:
                    # try:

                    # res = requests.get(url)

                    # res = self.pool.request('GET', url)
                    res = requests.get(url, stream=True)
                    if res.status_code == 200:
                        dirs = dirs.rstrip().split("\n")
                        print("[+] Doowloading ", dirs)
                        dirs = dirs[0]
                        dirs = dirs.replace(" ", "_")
                        # Copy Image
                        filename = dirs + str(count) + ".jpg"
                        # Make directory
                        print(f"[+] Writing file to /tmp/{filename}")
                        filename = "/tmp/" + filename
                        with open(filename, 'wb') as f:
                            shutil.copyfileobj(res.raw, f)
                            # shutil.copyfileobj(res.raw, f)
                        print("[+] Local upload complete. Uploading to S3")
                        with open(filename, 'rb') as f:
                            up_filename = filename.replace("/tmp/", "")
                            self.client.upload_fileobj(f, "sagemakertestwat", "data/" + dirs + "/" + up_filename)
                        os.remove(filename)
                        print("shoe {}".format(count))
                        print("Able to grab {}".format(count))
                        count += 1

        browser.close()
        return count


def main():
    for i in range(1, 34):
        yeezy = WATScrper(f"https://www.footlocker.com/category/shoes/new-releases.html?currentPage={i}",
                          "ProductName-primary", )
        yeezy.scrape_shoes()


if __name__ in "__main__":
    main()
