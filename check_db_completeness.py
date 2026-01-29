import sqlite3
from constants import STATIONS

def check_missing_pairs():
    db_name = "metro_data.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Get all pairs from DB
    cursor.execute("SELECT from_station_id, to_station_id FROM metro_fares")
    db_pairs = set(cursor.fetchall())
    conn.close()
    
    station_ids = sorted(STATIONS.keys())
    missing = []
    total_expected = 0
    
    for i, frm in enumerate(station_ids):
        for to in station_ids[i+1:]:
            total_expected += 1
            if (frm, to) not in db_pairs:
                missing.append((STATIONS[frm], STATIONS[to], frm, to))
                
    print(f"Total expected pairs: {total_expected}")
    print(f"Pairs in DB: {len(db_pairs)}")
    print(f"Missing pairs ({len(missing)}):")
    for frm_name, to_name, frm_id, to_id in missing:
        print(f"  - {frm_name} (ID: {frm_id}) <-> {to_name} (ID: {to_id})")

if __name__ == "__main__":
    check_missing_pairs()
