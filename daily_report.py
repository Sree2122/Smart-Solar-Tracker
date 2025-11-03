# daily_report.py
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from proxy_energy import compute_proxy_energy
from fpdf import FPDF
import os

CSV = "solar_energy_log.csv"
OUT_XLSX = "daily_report.xlsx"
OUT_PDF = "daily_summary.pdf"
PLOT_IMG = "daily_plot.png"

def parse_time(v):
    try:
        return datetime.strptime(str(v), "%Y-%m-%d %H:%M:%S")
    except:
        try:
            return datetime.fromtimestamp(float(v))
        except:
            return pd.NaT

def load_today():
    if not os.path.exists(CSV):
        return pd.DataFrame()
    df = pd.read_csv(CSV)
    if df.empty:
        return df
    df["__time"] = df.iloc[:,0].apply(parse_time)
    df = df.dropna(subset=["__time"])
    today = datetime.now().date()
    return df[df["__time"].dt.date == today].copy()

def make_plot(df):
    if df.empty: return None
    plt.figure(figsize=(8,4))
    # detect sensor columns
    cols = df.columns.tolist()
    if "Left" in cols and "Right" in cols:
        sensors = ["Left", "Right"]
    else:
        sensors = cols[1:3]
    for s in sensors:
        plt.plot(df["__time"], df[s], label=s)
    plt.legend()
    plt.xlabel("Time")
    plt.ylabel("LDR")
    plt.tight_layout()
    plt.savefig(PLOT_IMG)
    plt.close()
    return PLOT_IMG

def make_pdf(summary_text, plot_img):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.split("\n"):
        pdf.multi_cell(0, 8, line)
    pdf.ln(5)
    if plot_img and os.path.exists(plot_img):
        pdf.image(plot_img, w=180)
    pdf.output(OUT_PDF)
    print("Saved PDF:", OUT_PDF)

def build_report():
    df = load_today()
    if df.empty:
        print("No data for today. CSV missing or no rows for today.")
        return
    # Save Excel (full data for today)
    df.to_excel(OUT_XLSX, index=False)
    print("Excel saved:", OUT_XLSX)
    # Proxy energy
    proxy = compute_proxy_energy()
    # Basic stats
    total_samples = len(df)
    mean_vals = {}
    for col in df.columns[1:]:
        if pd.api.types.is_numeric_dtype(df[col]):
            mean_vals[col] = df[col].mean()
    # Plot
    img = make_plot(df)
    # Build summary text
    summary = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    summary += f"Total samples: {total_samples}\n"
    summary += "Mean sensor values:\n"
    for k,v in mean_vals.items():
        summary += f"  {k}: {v:.2f}\n"
    summary += f"\nProxy energy (arbitrary units): {proxy:.2f}\n"
    make_pdf(summary, img)

if _name_ == "_main_":
    build_report()