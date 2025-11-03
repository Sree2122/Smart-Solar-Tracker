# proxy_energy.py
import pandas as pd
from datetime import datetime
import os

print("Script started. Current folder:", os.getcwd())
print("Looking for CSV at:", os.path.abspath("solar_tracker_data.csv"))

CSV = "solar_tracker_data.csv"   # <-- match your real CSV file

def parse_time(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except:
            pass
    try:
        return datetime.fromtimestamp(float(s))
    except:
        return None

def compute_proxy_energy(csv_path=CSV, scale=1.0):
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return 0.0
    df = pd.read_csv(csv_path)
    if df.empty:
        print("CSV file is empty.")
        return 0.0

    cols = df.columns.tolist()
    tcol = cols[0]

    # detect which columns to use for LDR data
    if "TL" in cols and "TR" in cols:
        sensors = ["TL", "TR"]
    elif len(cols) >= 3:
        sensors = cols[1:3]
    else:
        print("No valid LDR columns found.")
        return 0.0

    # parse timestamps
    df["__time"] = df[tcol].apply(parse_time)
    df = df.dropna(subset=["__time"]).reset_index(drop=True)
    if len(df) < 2:
        print("Not enough data points to compute energy.")
        return 0.0

    # mean sensor value
    df["mean_ldr"] = df[sensors].astype(float).mean(axis=1)

    total = 0.0
    for i in range(1, len(df)):
        dt_hours = (df.loc[i, "__time"] - df.loc[i-1, "__time"]).total_seconds() / 3600.0
        avg = 0.5 * (df.loc[i, "mean_ldr"] + df.loc[i-1, "mean_ldr"])
        total += avg * dt_hours

    return total * scale

if __name__ == "__main__":
    val = compute_proxy_energy()
    print(f"Proxy energy (arbitrary units): {val:.4f}")
    with open("proxy_energy_output.txt", "w") as f:
        f.write(f"{val:.4f}")