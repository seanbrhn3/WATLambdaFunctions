"""
This script is used create directories for shoe scrapers to then be deployed into aws
"""
import os
import re


def copy_template_folder():
    scraper_name = input("What's the name of the scraper? ")
    os.mkdir(scraper_name)
    os.system(f"cp -r _template/  {scraper_name}/")


if __name__ == '__main__':
    copy_template_folder()
