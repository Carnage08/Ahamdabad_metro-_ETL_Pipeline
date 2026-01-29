import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_visualizations():
    # Setup directory for assets
    output_dir = "assets"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    conn = sqlite3.connect("metro_data.db")
    df = pd.read_sql_query("SELECT * FROM metro_fares", conn)
    conn.close()
    
    if df.empty:
        print("No data found.")
        return

    # Set style
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)

    # 1. Fare Distribution
    plt.figure()
    sns.histplot(df['fare'], bins=range(0, int(df['fare'].max()) + 5, 5), kde=True, color='#2c3e50')
    plt.title('Distribution of Metro Fares (INR)', fontsize=15)
    plt.xlabel('Fare (Rs.)')
    plt.ylabel('Frequency (Route Pairs)')
    plt.savefig(os.path.join(output_dir, 'fare_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Travel Time vs Fare Correlation
    plt.figure()
    sns.scatterplot(data=df, x='travel_time_min', y='fare', alpha=0.5, color='#e74c3c')
    plt.title('Correlation: Travel Time vs Fare', fontsize=15)
    plt.xlabel('Travel Time (Minutes)')
    plt.ylabel('Fare (Rs.)')
    plt.savefig(os.path.join(output_dir, 'time_fare_correlation.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Top 10 Stations by Connections (Frequency in route pairs)
    # Since we store unique pairs, we count how many times each station appears in from or to
    station_counts = pd.concat([df['from_station_name'], df['to_station_name']]).value_counts().head(10)
    plt.figure()
    sns.barplot(x=station_counts.values, y=station_counts.index, palette='viridis')
    plt.title('Top 10 Most Connected Stations', fontsize=15)
    plt.xlabel('Number of Route Pairs')
    plt.ylabel('Station Name')
    plt.savefig(os.path.join(output_dir, 'top_stations.png'), dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Visualizations generated successfully in {output_dir}/")

if __name__ == "__main__":
    generate_visualizations()
