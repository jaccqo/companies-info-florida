from PyQt5.QtCore import QThread, pyqtSignal
import time
from threading import Thread
from bot import scraperBot

class ScraperThread(QThread,scraperBot):
    worker_signal=pyqtSignal(str)

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def run(self):
        last_signal=""
       

        th=Thread(target=self.scrape_website,args=(self.keyword,))
        th.start()

        while not self.not_finished:
            if not last_signal == self.scraper_signal:
                self.worker_signal.emit(str(self.scraper_signal))
                last_signal=self.scraper_signal
               
            
