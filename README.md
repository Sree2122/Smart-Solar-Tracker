# Smart-Solar-Tracker
# ☀️ Solar Tracker Dashboard (Arduino + Python + Streamlit)

## 📘 Overview

This project is a **solar tracking system** that combines Arduino hardware with a **Python–based software dashboard** for real-time monitoring, data logging, and energy analysis.

The **hardware** (LDR sensors + servo motors + Arduino) tracks the sun’s position, while the **software stack**:

* Logs sensor and servo data (`solar_tracker_data.csv`)
* Computes **proxy solar energy** from light readings
* Generates visual dashboards and daily analytics reports

---

## 🧩 Features

### 🔹 Real-Time Data Logging

* Arduino sends LDR and servo readings via serial.
* Python logger saves values as `solar_tracker_data.csv`:

  ```
  Time, TL, TR, BL, BR, ServoX, ServoY
  ```

### 🔹 Proxy Energy Integrator (`proxy_energy.py`)

* Reads the CSV and computes total *proxy* solar energy.
* Outputs cumulative energy values and statistics.

### 🔹 Daily Report Generator (`daily_report.py`)

* Creates Excel + PDF reports with:

  * Summary statistics
  * Graphs of LDR readings and servo motion
  * Cumulative proxy energy trend
* Can be automated with **Windows Task Scheduler**.

### 🔹 Streamlit Dashboard (`streamlit_app.py`)

* Interactive live dashboard showing:

  * Real-time LDR and servo angle charts
  * Instantaneous and cumulative proxy energy
  * Current and total energy metrics
* Refreshable in-browser with one click.

---

## ⚙️ Folder Structure

```
solar-tracker/
│
├── solar_energy_logger.py      # Reads from Arduino serial and logs to CSV
├── proxy_energy.py             # Energy computation module
├── daily_report.py             # Generates daily Excel + PDF summaries
├── streamlit_app.py            # Live interactive dashboard
├── solar_tracker_data.csv      # Logged sensor + servo data
└── README.md                   # Project documentation
```

---

## 🧰 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/solar-tracker-dashboard.git
cd solar-tracker-dashboard
```

### 2. Install Python Dependencies

```bash
pip install pandas plotly streamlit openpyxl reportlab
```

### 3. Connect Arduino

* Upload your Arduino solar tracker sketch.
* Open **`solar_energy_logger.py`** to start logging data.
* Make sure your COM port matches the one in the code.

### 4. Run the Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Open the browser at `http://localhost:8501` to view the dashboard.

---

## 📊 Data Format

| Time (Unix) | TL  | TR  | BL  | BR  | ServoX | ServoY |
| ----------- | --- | --- | --- | --- | ------ | ------ |
| 1730750150  | 400 | 380 | 350 | 360 | 92     | 88     |

---

## ⚡ Proxy Energy Formula

```python
proxy_energy = ((TL + TR + BL + BR) / 4) * 0.001
```

Cumulative energy is computed as the running sum of all proxy energy values.

---

## 🧾 Automating Daily Reports (Windows Task Scheduler)

1. Open **Task Scheduler → Create Task**
2. Set trigger → “Daily at 6:00 PM”
3. Action → “Start a program”
4. Program/script:

   ```
   python
   ```

   Arguments:

   ```
   "C:\path\to\daily_report.py"
   ```
5. Save → Reports will be generated automatically every day.

---

## 🧠 Troubleshooting

| Issue                    | Possible Fix                                                                 |
| ------------------------ | ---------------------------------------------------------------------------- |
| CSV not updating         | Ensure `solar_energy_logger.py` is running and Serial Plotter is **closed**. |
| COM port error           | Update the correct port in `solar_tracker_dashboard.py` or logger script.    |
| Missing columns          | Verify your CSV headers: `Time, TL, TR, BL, BR, ServoX, ServoY`.             |
| Streamlit not refreshing | Click **Refresh Data** or restart the dashboard.                             |
| PDF report not generated | Ensure `reportlab` and `openpyxl` are installed.                             |

---

## 🧠 Future Enhancements

* Add **auto-refreshing Streamlit** dashboard every few seconds
* Cloud dashboard hosting (Streamlit Cloud / Heroku)
* Predictive tracking model using past light trends
* Integration with solar power sensors for real energy measurement

---

## 🧑‍💻 Author

**Sree Charan**

📫 Feel free to fork, improve, or connect!

---
