import json
from wat_scraper import WATScrper

"""
All scrapers need to handle pagination
"""


def pagination():
    pass


def lambda_handler(event, context):
    balenciaga = WATScrper("https://www.balenciaga.com/us/men/shoes", "c-product__name")
    shoes_found = balenciaga.scrape_shoes()

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(f'{shoes_found} uploaded')
    }
  



