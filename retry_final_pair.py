import logging
import time
from scraper import MetroScraper
from database import Database
from constants import STATIONS

def retry_final_pair():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    db = Database()
    scraper = MetroScraper()
    
    frm, to = 1, 2 # Vastral Gam <-> Nirant Cross Road
    
    try:
        logging.info(f"Retrying final pair with extra patience: {STATIONS[frm]} <-> {STATIONS[to]}")
        
        # Manual fetch logic with extra wait if needed
        data = scraper.fetch_route_data(frm, to)
        if data:
            db.insert_fare(data)
            logging.info(f"SUCCESS: Scraped final pair.")
        else:
            logging.error("STILL FAILED: Pair 1<->2 could not be scraped.")
            
    finally:
        scraper.close()

if __name__ == "__main__":
    retry_final_pair()
