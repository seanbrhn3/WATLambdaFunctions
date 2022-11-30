from distutils.log import ERROR
import json
from wat_scraper import WATScraper
import logging
"""
All scrapers need to handle pagination
"""
logging.basicConfig(level=logging.ERROR)

def pagination():
    pass


def lambda_handler(event, context):
    try:
        # The second parameter should be the tile class for the
        balenciaga = WATScraper("https://www.balenciaga.com/us/men/shoes", "l-productgrid__item")
        shoes_found = balenciaga.scrape_shoes()
    except Exception as e:
        logging.error(f"[!] Error scraping shoes: {e}")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(f'{shoes_found} uploaded')
    }
  

print(lambda_handler(None,None))
