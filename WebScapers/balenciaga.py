from watScraper import WATScrper

"""
All scrapers need to handle pagination
"""


def pagination():
    pass


def main():
    balenciaga = WATScrper("https://www.balenciaga.com/us/men/shoes", "c-product__name")
    balenciaga.scrape_shoes()


if __name__ in "__main__":
    main()
