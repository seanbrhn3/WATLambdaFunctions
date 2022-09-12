from distutils.log import ERROR
import json
from wat_scraper import WATScrper
import logging
"""
All scrapers need to handle pagination
"""
logging.basicConfig(level=logging.ERROR)

def pagination():
    pass


def lambda_handler(event, context):
    try:
        balenciaga = WATScrper("https://www.balenciaga.com/us/men/shoes", "c-product__name")
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
  



