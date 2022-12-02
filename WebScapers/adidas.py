from watScraper import WATScrper



def main():
    count = 0
    while count <= 192:
        best_selling_men = WATScrper(f"https://www.adidas.com/us/women-shoes?start={count}","gl-paragraph gl-paragraph--s glass-product-card__title")
        best_selling_men.scrape_shoes()
        # women = WATScrper("https://www.adidas.com/us/women-shoes?start={}".format(count),"plp-grid___hCUwO")
        # slides = WATScrper("https://www.adidas.com/us/men-slides?start={}".format(count),"grid-item___3rAkS")
        # all_men = WATScrper("https://www.adidas.com/us/men-shoes?start={}".format(count),"grid-item___3rAkS")
        # running = WATScrper("https://www.adidas.com/us/men-running-shoes?start={}".format(count), "grid-item___3rAkS")
        # adidas = WATScrper("https://www.adidas.com/us/men-athletic_sneakers?start={}".format(count),"grid-item___3rAkS")
        #
        # women.scrape_shoes()
        # slides.scrape_shoes()
        # all_men.scrape_shoes()
        # running.scrape_shoes()
        # adidas.scrape_shoes()
        count += 48

if __name__ in "__main__":
    main()
