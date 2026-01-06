import csv
import time
import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# Load environment variables
load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
trigger_url = os.environ.get("TRIGGER_URL")

if not url or not key:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file")
    exit(1)

supabase: Client = create_client(url, key)

def main():
    filename = "data.csv"
    while True:
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            # Load the data first
            try:
                with open(filename, "r", newline="") as f:
                    reader = csv.reader(f)
                    rows = list(reader)
            except Exception as e:
                print(f"Error reading file: {e}")
                rows = []
            
            # Clear the csv
            try:
                with open(filename, "w", newline="") as f:
                    pass # Opening in 'w' mode truncates the file
            except Exception as e:
                print(f"Error clearing file: {e}")

            # Process and send data
            data_to_insert = []
            for row in rows:
                if not row: continue
                if row[0] == "room": continue # Skip header

                # Print as requested
                # print(row)

                try:
                    record = {
                        "room_id": row[0],
                        "room_type": row[1],
                        "recorded_time": row[2],
                        "temperature_c": float(row[3]),
                        "humidity_pct": float(row[4]),
                        "differential_pressure_pa": float(row[5]),
                    }
                    data_to_insert.append(record)
                except (ValueError, IndexError) as e:
                    print(f"Error parsing row {row}: {e}")

            if data_to_insert:
                try:
                    supabase.table("readings_v2").insert(data_to_insert).execute()
                    print(f"{datetime.now().replace(microsecond=0)} - Sent {len(data_to_insert)} records to Cloud Database.")
                    
                    if trigger_url:
                        try:
                            requests.post(trigger_url)
                        except Exception as e:
                            pass
                except Exception as e:
                    print(f"Error sending to Cloud Database: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
