import serial
import csv
import time

# === CONFIGURATION ===
PORT = 'COM5'   # your Arduino COM port
BAUD = 9600
FILENAME = "solar_tracker_data.csv"

# === SETUP ===
print(f"Connecting to {PORT}...")
ser = serial.Serial(PORT, BAUD, timeout=2)
time.sleep(2)  # give Arduino time to reset

# clear old CSV and start fresh
with open(FILENAME, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "TL", "TR", "BL", "BR", "ServoX", "ServoY"])

print("\n✅ Logging started! Press Ctrl+C to stop.\n")

try:
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            continue

        parts = line.split(',')
        if len(parts) != 6:
            continue  # skip bad lines

        now = time.strftime("%Y-%m-%d %H:%M:%S")
        row = [now] + parts

        with open(FILENAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        print("📡", ",".join(row))

except KeyboardInterrupt:
    print("\n🛑 Logging stopped by user.")
    ser.close()
