import streamlit as st
import pandas as pd
import numpy as np
import time

# Konfigurasi Halaman
st.set_page_config(page_title="Nexus Omniwheel 4WD Monitoring", layout="wide")

st.title("🤖 Nexus Omniwheel 4WD Real-Time Dashboard")
st.markdown("Monitoring Robot: **Apriyana Putra - Politeknik Negeri Batam**")

# --- SIDEBAR: KONTROL & STATUS ---
st.sidebar.header("Robot Status")
battery = st.sidebar.progress(85, text="Battery: 85%")
mode = st.sidebar.selectbox("Control Mode", ["Manual", "Auto-Pilot", "Fuzzy Correction"])
if st.sidebar.button("Reset Odometry"):
    st.sidebar.warning("Odometry Reset!")

# --- DATA SIMULATION (Logika Robot) ---
def get_robot_data():
    # Simulasi data dari IMU dan Encoder
    return {
        "heading": np.random.uniform(0, 360), # Data IMU (Yaw)
        "pitch": np.random.uniform(-5, 5),    # Data IMU (Pitch)
        "m1_rpm": np.random.randint(100, 110),
        "m2_rpm": np.random.randint(100, 110),
        "m3_rpm": np.random.randint(100, 110),
        "m4_rpm": np.random.randint(100, 110),
        "x": np.random.uniform(0, 10),
        "y": np.random.uniform(0, 10)
    }

# --- MAIN DASHBOARD LAYOUT ---
col1, col2, col3 = st.columns(3)

# Baris 1: Metrik Utama
data = get_robot_data()
col1.metric("IMU Heading (Yaw)", f"{data['heading']:.2f}°", delta="Target: 0°")
col2.metric("Avg Motor Speed", "105 RPM")
col3.metric("System Stability", "Excellent")

st.divider()

# Baris 2: Visualisasi Motor & Pergerakan
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Motor Synchronization (Encoder Data)")
    # Simulasi grafik realtime
    chart_data = pd.DataFrame(
        np.random.randn(20, 4),
        columns=['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4']
    )
    st.line_chart(chart_data)

with right_col:
    st.subheader("Orientation (IMU)")
    # Menampilkan posisi robot secara sederhana
    st.write(f"Pitch: {data['pitch']:.2f}°")
    st.write(f"Roll: {np.random.uniform(-2, 2):.2f}°")
    # Representasi visual sederhana untuk arah (Heading)
    st.info(f"Robot saat ini menghadap: {data['heading']:.1f} derajat")

# Baris 3: Mapping / Odometry
st.subheader("Robot Path Tracking (X-Y Plane)")
map_data = pd.DataFrame(
    np.random.randn(10, 2) / [50, 50] + [1.12, 104.0], # Contoh koordinat Batam
    columns=['lat', 'lon']
)
st.map(map_data)

# Auto-refresh simulasi
time.sleep(0.5)
st.rerun()
