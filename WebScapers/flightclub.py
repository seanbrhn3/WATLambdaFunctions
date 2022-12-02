from watScraper import WATScrper


def main():
    for i in range(20, 34):
        yeezy = WATScrper(f"https://www.flightclub.com/sneakers?page={i}", ".sc-fbHdRr.kalwxn", element="img")
        yeezy.scrape_shoes()


if __name__ in "__main__":
    main()
