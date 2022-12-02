from watScraper import WATScrper

def main():
    count = 1
    while count < 100:
        men = WATScrper("https://www.kicksonfire.com/app/upcoming?page={}","main")
        men.scrape_shoes()
        count += 1
        print("COUNT AT {}".format(count))

if __name__ in "__main__":
    main()