import logging
import time
import pandas as pd
from scraper import MetroScraper
from database import Database
from constants import STATIONS

def main():
    db = Database()
    scraper = MetroScraper()
    
    # Total stations: 54
    station_ids = sorted(STATIONS.keys())
    
    all_data = []
    
    try:
        # Only scrape unique pairs (frm < to) since fares are symmetric
        # This reduces 54×53 = 2,862 pairs to 54×53/2 = 1,431 pairs
        for i, frm in enumerate(station_ids):
            for to in station_ids[i+1:]:  # Only pairs where frm < to
                data = scraper.fetch_route_data(frm, to)
                if data:
                    db.insert_fare(data)
                    all_data.append(data)
                    logging.info(f"Saved: {data['from_station_name']} ↔ {data['to_station_name']}")
                
                time.sleep(1) # Polite scraping
                
    finally:
        scraper.close()
    
    # Generate summary CSV
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv("metro_fare_summary.csv", index=False)
        logging.info("Summary CSV generated: metro_fare_summary.csv")

if __name__ == "__main__":
    main()
