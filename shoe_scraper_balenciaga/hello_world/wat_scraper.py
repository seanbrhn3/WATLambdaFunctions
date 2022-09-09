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
TODO:
    1. ChromeDriverManager().install() download the chrome driver but the lambda function has READ ONLY ACCESS TO /home/sbx_user1051
    which is where  it apprently writes too.
    
    Probably need to configure cloudformation template to allow writable access to /home/
    
    This helps:https://stackoverflow.com/questions/71746654/how-do-i-add-selenium-chromedriver-to-an-aws-lambda-function
    
"""
class WATScrper:
    # gfs = GoogleImagesSearch(key_and_id["key"], key_and_id["id"])
    gfs = google_images_download.googleimagesdownload()
    client = boto3.client("s3")
    tile_class = None
    image_links = []
    link = None
    pool = urllib3.PoolManager()

    def __init__(self, link,tile_class,element=None):
        self.link = link
        self.element = element
        self.tile_class = tile_class

    def scrape_shoes(self):
        # Random headers the make the site believe we're a real browser
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/81.0.4044.141 Safari/537.36"
        }
        if self.link is not None:
            print("here", self.link)
            sneaker_head = requests.get(self.link, headers=headers)
        else:
            return "link is null"
        # try:
        sneaker_head_object = BeautifulSoup(sneaker_head.content, "html.parser")
        if self.element is None:
            sneaker_head_image = sneaker_head_object.find_all(class_=self.tile_class)
        else:
            sneaker_head_image = sneaker_head_object.find_all(self.element,class_=self.tile_class)
        print(f"found {len(sneaker_head_image)} shoes")
        found_title = "None"
        for sneaker in sneaker_head_image:
            print(f"Gathering data on {sneaker.getText()}")
            found_title = sneaker.getText()
            print("here's what was found", found_title)
            self.image_links.append(found_title)

            self.client.put_object(Bucket="sagemakertestwat-dev", Key=found_title)
            # adds image to directory
            images_found = self.download_google_staticimages(found_title)
            return f"{images_found} images collected"
        # except Exception as e:
        #     print(f"Unable to find shoe names: {e}")

    """
    function name: download_google_staticimage,
    purpose: use the google_images_download library to download the she image passed in the scrape shoes function.
    This image is downloaded from goole and put in the downloads directory. I call get_images to put the image in 
    in the shoe directory for the machine learning  algo, and then send the images into the  dev/prod s3 bucket
    """

    def download_google_staticimages(self, dirs):
        dirs = dirs.replace(" ", "-")
        search_url = 'https://www.google.com/search?q=' + dirs + '&source=lnms&tbm=isch'
        print(f"Grabbing images for {dirs}")
        options = selenium.webdriver.ChromeOptions()
        options.add_argument('--headless')  # Chrome will operate in the background and won't open a window
        options.add_argument('--no-sandbox')
        options.binary_location = '/opt/chrome/chrome'
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--no-first-run')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-client-side-phishing-detection')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-web-security')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument("--remote-debugging-port=9222")
        browser = selenium.webdriver.Chrome("/opt/chromedriver", options=options)
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
                        print("[+] Doowloading ",dirs)
                        dirs = dirs[0]
                        dirs = dirs.replace(" ", "_")
                        # Copy Image
                        filename = dirs + str(count) + ".jpg"
                        # Make directory
                        print(f"[+] Writing file to /tmp/{filename}")
                        with open(f"/tmp/{filename}", 'wb') as f:
                            shutil.copyfileobj(res.raw, f)
                            # shutil.copyfileobj(res.raw, f)
                        print("[+] Local upload complete. Uploading to S3")
                        with open(f"/tmp/{filename}", 'rb') as f:
                            self.client.upload_fileobj(f, "sagemakertestwat-dev", dirs + "/" + filename)
                        os.remove(f"/tmp/{filename}")
                        print("shoe {}".format(count))
                        print("Able to grab {}".format(count))
                        count += 1

        browser.close()
        return count

