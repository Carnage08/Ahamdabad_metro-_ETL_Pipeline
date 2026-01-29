import re
import logging

def clean_fare(fare_text):
    """Extracts numeric fare from string like 'Fare Rs. 10'"""
    if not fare_text:
        return 0.0
    match = re.search(r'(\d+)', fare_text)
    if match:
        return float(match.group(1))
    logging.warning(f"Could not parse fare from: '{fare_text}'")
    return 0.0

def clean_time(time_text):
    """Extracts minutes from string like '5Min' or '10 Min'"""
    if not time_text:
        return 0
    match = re.search(r'(\d+)', time_text)
    if match:
        return int(match.group(1))
    logging.warning(f"Could not parse time from: '{time_text}'")
    return 0

def clean_station_count(count_text):
    """Extracts number of stations from string like 'Stations 3'"""
    if not count_text:
        return 0
    match = re.search(r'(\d+)', count_text)
    if match:
        return int(match.group(1))
    logging.warning(f"Could not parse station count from: '{count_text}'")
    return 0
