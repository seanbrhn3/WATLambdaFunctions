from watScraper import WATScrper
def main():
    count = 0
    while count < 121:
        men = WATScrper(f"https://www.dsw.com/en/us/brands/vans/N-1z14145?No={count}",
                        "product-tile__name product-tile__name--margin title--sentence title--body body-12 ng-star-inserted")
        men.scrape_shoes()
        count += 60


if __name__ in "__main__":
    main()
