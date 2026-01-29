import logging
import sys
import os

# Add the current directory to path so we can import our modules
sys.path.append(os.getcwd())

from scraper import MetroScraper

def test_route(frm_id, to_id):
    scraper = MetroScraper()
    try:
        print(f"\nTesting route {frm_id} to {to_id}...")
        data = scraper.fetch_route_data(frm_id, to_id)
        if data:
            print(f"From: {data['from_station_name']}")
            print(f"To: {data['to_station_name']}")
            print(f"Fare: {data['fare']}")
            print(f"Time: {data['travel_time_min']} min")
            print(f"Stations Count: {data['stations_count']}")
            print(f"Intermediate Stations: {data['intermediate_stations']}")
            
            # Basic assertions
            assert data['fare'] > 0, "Fare should be greater than 0"
            assert data['stations_count'] > 0, "Station count should be greater than 0"
            assert len(data['intermediate_stations'].split(",")) > 0, "Should have intermediate stations"
            print("Status: SUCCESS")
        else:
            print("Status: FAILED (No data returned)")
    finally:
        scraper.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test 1: Direct Route (Vastral Gam to Rabari Colony)
    # IDs: 1 to 4
    try:
        test_route(1, 4)
    except AssertionError as e:
        print(f"Test 1 Assertion Failed: {e}")

    # Test 2: Interchange Route (Vastral Gam to APMC)
    # IDs: 1 to 19
    try:
        test_route(1, 19)
    except AssertionError as e:
        print(f"Test 2 Assertion Failed: {e}")
