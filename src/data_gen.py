import random
from datetime import datetime, timedelta
from time import sleep
import os
import csv

ROOMS = [(f"Room {i}", 'type-A5') for i in range(1, 7)]
SAMPLES_PER_ROOM = 1

def generate_reading():
    # temperature in °C, humidity in %, differential pressure in Pa
    # mimic Arduino sensors with slow drift, small gaussian noise, occasional spike and quantization
    if not hasattr(generate_reading, "_state"):
        generate_reading._state = {
            "temp": 22.0 + random.uniform(-1.0, 1.0),
            "hum": 45.0 + random.uniform(-5.0, 5.0),
            "dp": 0.0 + random.uniform(-0.5, 0.5),
            "offset_temp": random.uniform(-0.2, 0.2),  # small calibration offset
            "offset_hum": random.uniform(-0.5, 0.5),
            "offset_dp": random.uniform(-0.1, 0.1),
        }

    s = generate_reading._state

    # small random walk to simulate sensor inertia / environmental change
    s["temp"] += random.gauss(0, 0.05)  # °C step
    s["hum"] += random.gauss(0, 0.2)    # % step
    s["dp"] += random.gauss(0, 0.02)    # Pa step

    # occasional transient spike/drop (e.g., door open, draft)
    if random.random() < 0.015:
        s["temp"] += random.choice([-1, 1]) * random.uniform(0.5, 2.0)
    if random.random() < 0.01:
        s["hum"] += random.choice([-1, 1]) * random.uniform(1.0, 6.0)
    if random.random() < 0.01:
        s["dp"] += random.choice([-1, 1]) * random.uniform(0.5, 3.0)

    # clamp to realistic sensor ranges
    s["temp"] = max(0.0, min(50.0, s["temp"]))
    s["hum"] = max(0.0, min(100.0, s["hum"]))
    s["dp"] = max(-50.0, min(50.0, s["dp"]))

    # apply small calibration offsets and quantize to mimic ADC/resolution limits
    temperature_c = round(s["temp"] + s["offset_temp"], 2)          # give 2 decimals like many conversions
    humidity_pct = round(s["hum"] + s["offset_hum"], 1)             # humidity often reported to 0.1%
    differential_pressure_pa = round(s["dp"] + s["offset_dp"], 2)   # small Pa resolution

    return {
        "temperature_c": temperature_c,
        "humidity_pct": humidity_pct,
        "differential_pressure_pa": differential_pressure_pa,
    }

def generate_room_data(num_samples):
    # create slightly staggered timestamps for readability
    base = datetime.now()
    return [
        {**generate_reading(), "timestamp": (base + timedelta(seconds=i)).isoformat() + "Z"}
        for i in range(num_samples)
    ]

def main():
    print("Info: Data Simulation Started ...")
    print("Saving data in csv file ...")
    
    while True:
        filename = "data.csv"
        need_header = (not os.path.exists(filename)) or (os.path.getsize(filename) == 0)

        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            for room in ROOMS:
                readings = generate_room_data(SAMPLES_PER_ROOM)
                for r in readings:
                    writer.writerow([room[0], room[1], r["timestamp"], r["temperature_c"], r["humidity_pct"], r["differential_pressure_pa"]])
        sleep(1)  # simulate delay between room reading

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInfo: Data Simulation Stopped.")