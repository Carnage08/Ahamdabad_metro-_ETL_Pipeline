import pandas as pd
import sqlite3
import logging

def generate_summary():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    conn = sqlite3.connect("metro_data.db")
    df = pd.read_sql_query("SELECT * FROM metro_fares", conn)
    conn.close()
    
    if not df.empty:
        output_file = "metro_fare_summary.csv"
        df.to_csv(output_file, index=False)
        logging.info(f"Successfully generated {output_file} with {len(df)} records.")
    else:
        logging.warning("No data found in database to generate summary.")

if __name__ == "__main__":
    generate_summary()
