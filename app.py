import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Nexus Omni 4WD Monitor", layout="wide")

# Custom CSS untuk tampilan lebih profesional
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 Nexus Omniwheel 4WD Telemetry")
st.write("Project-Based Learning - Teknik Robotika Politeknik Negeri Batam")

# --- SIDEBAR CONTROL ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/id/c/c9/Logo_Polibatam.png", width=100)
st.sidebar.header("Robot Control Panel")
status = st.sidebar.status("Robot Connected", state="running")
mode = st.sidebar.selectbox("Drive Mode", ["Field-Oriented", "Robot-Centric", "Fuzzy Auto-Correction"])
st.sidebar.divider()
st.sidebar.write("**System Health**")
cpu_temp = st.sidebar.slider("Controller Temp", 30, 90, 45)

# --- SIMULASI DATA KINEMATIKA & IMU ---
# Dalam implementasi asli, data ini diambil dari sensor robot
def generate_telemetry():
    t = time.time()
    return {
        "yaw": (np.sin(t * 0.5) * 20) % 360, # Simulasi Heading IMU
        "pitch": np.sin(t) * 2,
        "roll": np.cos(t) * 1.5,
        "m1": 100 + np.random.randint(-5, 5),
        "m2": 100 + np.random.randint(-5, 5),
        "m3": 100 + np.random.randint(-5, 5),
        "m4": 100 + np.random.randint(-5, 5),
        "x": np.sin(t * 0.2) * 2, # Pergerakan di dalam kelas (meter)
        "y": t % 5               # Pergerakan maju (meter)
    }

data = generate_telemetry()

# --- BARIS 1: METRIK UTAMA ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Heading (IMU)", f"{data['yaw']:.1f}°", "Gyro Active")
m2.metric("Posisi X", f"{data['x']:.2f} m")
m3.metric("Posisi Y", f"{data['y']:.2f} m")
m4.metric("Battery", "12.4V", "-0.2V")

st.divider()

# --- BARIS 2: VISUALISASI UTAMA ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📍 Indoor Path Tracking (Classroom Scale)")
    # Path tracking menggunakan Plotly (X-Y Plane)
    fig_path = go.Figure()
    # Simulasi jejak (trail)
    trail_x = np.linspace(0, data['x'], 20)
    trail_y = np.linspace(0, data['y'], 20)
    
    fig_path.add_trace(go.Scatter(x=trail_x, y=trail_y, mode='lines', name='Path', line=dict(color='cyan', width=2)))
    fig_path.add_trace(go.Scatter(x=[data['x']], y=[data['y']], mode='markers+text', 
                                 name='Robot Pos', marker=dict(size=15, color='red', symbol='triangle-up')))
    
    fig_path.update_layout(
        xaxis=dict(range=[-3, 3], gridcolor='gray'),
        yaxis=dict(range=[0, 6], gridcolor='gray'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        height=400,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig_path, use_container_width=True)

with col_right:
    st.subheader("⚙️ Motor Synchronization (RPM)")
    # Data motor untuk grafik
    motor_df = pd.DataFrame({
        'Motor': ['M1', 'M2', 'M3', 'M4'],
        'RPM': [data['m1'], data['m2'], data['m3'], data['m4']]
    })
    st.bar_chart(motor_df.set_index('Motor'))
    
    # Indikator Kemiringan IMU
    st.write("**IMU Stability (Pitch & Roll)**")
    st.progress(abs(data['pitch']/10), text=f"Pitch: {data['pitch']:.1f}°")
    st.progress(abs(data['roll']/10), text=f"Roll: {data['roll']:.1f}°")

# --- BARIS 3: TABEL DATA MENTAH ---
with st.expander("Lihat Data Mentah (Telemetri)"):
    raw_data = pd.DataFrame([data])
    st.write(raw_data)

# Auto-refresh dashboard
time.sleep(0.1)
st.rerun()
