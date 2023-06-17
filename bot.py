import time


class scraperBot:
    def __init__(self):
        self.scraper_signal=""
        self.not_finished=False
    def scrape_website(self,keyword):

        for k,word in enumerate(keyword):
      

            self.scraper_signal=word

            # this emits last

            if k+1==len(keyword):
                self.scraper_signal="Scraping completed!"
            
            time.sleep(2)

        
        self.not_finished=True