import logging
import time
from scraper import MetroScraper
from database import Database
from constants import STATIONS

def scrape_specific_pairs():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    db = Database()
    scraper = MetroScraper()
    
    # Missing pairs identified
    missing_pairs = [
        (1, 2),   # Vastral Gam <-> Nirant Cross Road
        (2, 48),  # Nirant Cross Road <-> Akshardham
        (2, 49),  # Nirant Cross Road <-> Juna Sachivalaya
        (20, 46)  # Jivraj Park <-> Sector 10A
    ]
    
    scraped_count = 0
    
    try:
        for frm, to in missing_pairs:
            logging.info(f"Targeting missing pair: {STATIONS[frm]} ({frm}) <-> {STATIONS[to]} ({to})")
            data = scraper.fetch_route_data(frm, to)
            if data:
                db.insert_fare(data)
                scraped_count += 1
                logging.info(f"Successfully saved missing pair: {data['from_station_name']} ↔ {data['to_station_name']}")
            else:
                logging.error(f"Failed to scrape missing pair: {STATIONS[frm]} <-> {STATIONS[to]}")
            
            time.sleep(2) # Be extra polite for these few requests
            
    finally:
        scraper.close()
        logging.info(f"Finished scraping missing pairs. Total new records: {scraped_count}")

if __name__ == "__main__":
    scrape_specific_pairs()
