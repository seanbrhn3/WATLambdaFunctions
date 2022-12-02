from watScraper import WATScrper


def main():
    yeezy = WATScrper(f"https://www.flightclub.com/nike/new-releases?page={i}", ".sc-fbHdRr.kalwxn", element="img")
    yeezy.scrape_shoes()
    for i in range(1, 34):
        yeezy = WATScrper(f"https://www.flightclub.com/nike/new-releases?page={i}", ".sc-fbHdRr.kalwxn", element="img")
        yeezy.scrape_shoes()


if __name__ in "__main__":
    main()
