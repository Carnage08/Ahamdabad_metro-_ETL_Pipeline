import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from constants import BASE_URL, STATIONS
from utils import clean_fare, clean_time, clean_station_count

class MetroScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def fetch_route_data(self, frm_id, to_id):
        url = BASE_URL.format(frm=frm_id, to=to_id)
        logging.info(f"Fetching: {url}")
        
        try:
            self.driver.get(url)
            
            # 1. Wait for fare price
            wait = WebDriverWait(self.driver, 10)
            try:
                wait.until(lambda d: d.find_element(By.ID, 'fare-price').text.strip() != "")
            except Exception:
                logging.warning(f"Timeout waiting for fare data at {url}")

            # 2. Wait for route list to populate (at least one station link)
            try:
                wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#svgmap-content a")) > 0)
            except Exception:
                logging.warning(f"Timeout waiting for station list at {url}")
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Use correct element IDs for fare data
            fare_el = soup.find(id='fare-price')
            time_el = soup.find(id='fare-min')
            count_el = soup.find(id='stat-cnt')
            
            if not fare_el or not fare_el.get_text(strip=True):
                logging.warning(f"No valid fare data found for {frm_id} to {to_id}")
                return None

            fare_text = fare_el.get_text(strip=True)
            time_text = time_el.get_text(strip=True) if time_el else ""
            count_text = count_el.get_text(strip=True) if count_el else ""

            # Extract ALL station names from #svgmap-content
            route_stations = []
            container = soup.find(id='svgmap-content')
            if container:
                station_links = container.find_all('a')
                logging.info(f"Found {len(station_links)} links in #svgmap-content")
                for a in station_links:
                    name = a.get_text(strip=True)
                    # Filter out UI toggles and duplicates
                    if name and name not in ["Show All Station", "Hide All Station", "Interchange"] and name not in route_stations:
                        route_stations.append(name)
            
            if not route_stations:
                logging.warning(f"No route stations extracted for {frm_id} to {to_id}")
                # Log a snippet of the container for debugging
                if container:
                    logging.debug(f"Container HTML snippet: {str(container)[:500]}")

            return {
                'from_station_id': frm_id,
                'from_station_name': STATIONS.get(frm_id),
                'to_station_id': to_id,
                'to_station_name': STATIONS.get(to_id),
                'fare': clean_fare(fare_text),
                'travel_time_min': clean_time(time_text),
                'stations_count': clean_station_count(count_text),
                'intermediate_stations': ", ".join(route_stations)
            }
        except Exception as e:
            logging.error(f"Error scraping {frm_id} to {to_id}: {e}")
            return None

    def close(self):
        self.driver.quit()
