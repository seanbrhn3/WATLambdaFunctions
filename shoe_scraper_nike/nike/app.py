import json
from wat_scraper import WATScrper

def lambda_handler(event, context):
 # new_releases = WATScrper("https://www.nike.com/w/new-mens-shoes-3n82yznik1zy7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")
    # new_releases.scrape_shoes()
    # nike_kids = WATScrper("https://www.nike.com/w/boys-shoes-1onrazy7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")
    # nike_kids.scrape_shoes()
    # nike_women = WATScrper("https://www.nike.com/w/womens-shoes-5e1x6zy7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")
    # nike_women.scrape_shoes()
    # nike = WATScrper("https://www.nike.com/w/mens-shoes-nik1zy7ok","product-grid__items css-yj4gxb css-r6is66 css-1tvazw1 css-1oud6ob")
    # nike.scrape_shoes()

    jordans = WATScrper("https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok","product-grid__items css-hvew4t")

    bunches = WATScrper("https://www.nike.com/w/shoes-y7ok","product-grid__items css-hvew4t")

    #jordans.scrape_shoes()
    bunches.scrape_shoes()
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": json.dumps(f'{bunches} uploaded'),
            }
        ),
    }
