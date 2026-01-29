import sqlite3
import logging

class Database:
    def __init__(self, db_name="metro_data.db"):
        self.db_name = db_name
        self.setup_db()

    def setup_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metro_fares (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_station_id INTEGER,
                from_station_name TEXT,
                to_station_id INTEGER,
                to_station_name TEXT,
                fare FLOAT,
                travel_time_min INTEGER,
                stations_count INTEGER,
                intermediate_stations TEXT,
                UNIQUE(from_station_id, to_station_id)
            )
        ''')
        conn.commit()
        conn.close()

    def insert_fare(self, data):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO metro_fares (
                    from_station_id, from_station_name, 
                    to_station_id, to_station_name, 
                    fare, travel_time_min, 
                    stations_count, intermediate_stations
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['from_station_id'], data['from_station_name'],
                data['to_station_id'], data['to_station_name'],
                data['fare'], data['travel_time_min'],
                data['stations_count'], data['intermediate_stations']
            ))
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
        finally:
            conn.close()

    def get_all_data(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM metro_fares")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_fare(self, from_id, to_id):
        """Get fare between two stations (works in both directions)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        # Check both directions since we only store unique pairs (frm < to)
        cursor.execute('''
            SELECT fare, travel_time_min, stations_count, intermediate_stations
            FROM metro_fares 
            WHERE (from_station_id = ? AND to_station_id = ?)
               OR (from_station_id = ? AND to_station_id = ?)
        ''', (from_id, to_id, to_id, from_id))
        result = cursor.fetchone()
        conn.close()
        return result
