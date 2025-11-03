import serial
import time
import csv
from datetime import datetime

# Change this if your port is different
ser = serial.Serial('COM5', 9600, timeout=1)

# Open (or create) CSV file
with open("solar_energy_log.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Left", "Right", "Servo", "Energy_Wh"])

    energy_Wh = 0.0

    while True:
        try:
            line = ser.readline().decode(errors='ignore').strip()
            if line.startswith("Left:"):
                # Parse line: Left: 890 | Right: 760 | Servo: 95
                parts = line.replace(" ", "").split("|")
                left = int(parts[0].split(":")[1])
                right = int(parts[1].split(":")[1])
                servo = int(parts[2].split(":")[1])

                avg_light = (left + right) / 2
                energy_Wh += avg_light * 0.0001

                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([now, left, right, servo, round(energy_Wh, 3)])
                file.flush()

                print(f"{now} | L:{left} R:{right} Servo:{servo} | Energy={round(energy_Wh,3)} Wh")
            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nLogging stopped.")
        break