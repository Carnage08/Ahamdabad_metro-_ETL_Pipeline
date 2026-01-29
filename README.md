# Ahmedabad Metro Scraper

A robust web scraper to extract route and fare information for the Ahmedabad Metro. This project uses Selenium and BeautifulSoup to navigate the official Gujarat Metro website and stores the data in a SQLite database and a CSV summary.

## Setup

1. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies** (if not already installed):
   ```bash
   pip install selenium beautifulsoup4 webdriver-manager pandas lxml
   ```

## Execution

### 1. Run the Full Scraper
To scrape all station pairs (54 stations, ~1431 unique routes):
```bash
python main.py
```
*Note: This takes approximately 30-45 minutes due to polite delays between requests.*

### 2. Verify Data Completeness
Check if all 1431 pairs are present in the database:
```bash
python check_db_completeness.py
```

### 3. Fill Missing Gaps (if any)
If some pairs were missed due to network timeouts:
```bash
python scrape_missing.py
```

### 4. Export to CSV
Re-generate the `metro_fare_summary.csv` from the latest database data:
```bash
python export_to_csv.py
```

## Project Structure

- `main.py`: Entry point for full scraping.
- `scraper.py`: Core logic for Selenium-based extraction.
- `database.py`: SQLite database management.
- `constants.py`: Station IDs and URLs.
- `utils.py`: Data cleaning utilities.
- `metro_data.db`: SQLite database storing all fare data.
- `metro_fare_summary.csv`: Flattened CSV export for easy analysis.
