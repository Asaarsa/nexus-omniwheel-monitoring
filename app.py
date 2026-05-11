import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Nexus Omni 4WD Control", layout="wide")

# Custom CSS untuk tampilan profesional dan centering
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #262730; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #ff4b4b; border: 1px solid white; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    .command-text { text-align: center; color: #ff4b4b; font-family: monospace; font-size: 24px; padding: 10px; border: 1px solid #ff4b4b; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZING SESSION STATE ---
if 'active_mode' not in st.session_state:
    st.session_state.active_mode = "📊 Monitoring"
if 'last_command' not in st.session_state:
    st.session_state.last_command = "WAITING"

# --- SIDEBAR: KONTROL MODE & KONFIRMASI ---
st.sidebar.title("🤖 Robot Control")
st.sidebar.write("Team PBL - Polibatam")

selected_mode = st.sidebar.radio(
    "Pilih Mode Operasi:",
    ["📊 Monitoring", "🎮 Manual Control", "🤖 Auto Mode"],
    index=0
)

st.sidebar.divider()
if st.sidebar.button("✅ KONFIRMASI MODE", type="primary"):
    st.session_state.active_mode = selected_mode
    st.sidebar.success(f"Mode {selected_mode} Aktif!")

st.sidebar.info(f"Status: **{st.session_state.active_mode}**")

# --- FUNGSI SIMULASI DATA ---
def get_telemetry():
    return {
        "yaw": np.random.uniform(0, 360),
        "pitch": np.random.uniform(-1, 1),
        "roll": np.random.uniform(-1, 1),
        "m1": np.random.randint(95, 105),
        "m2": np.random.randint(95, 105),
        "m3": np.random.randint(95, 105),
        "m4": np.random.randint(95, 105),
        "x": np.random.uniform(-1.5, 1.5),
        "y": np.random.uniform(0, 4)
    }

data = get_telemetry()

# --- LOGIKA TAMPILAN BERDASARKAN MODE ---

st.title(f"{st.session_state.active_mode}")

if st.session_state.active_mode == "📊 Monitoring":
    # --- UI MONITORING ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Yaw (Heading)", f"{data['yaw']:.1f}°")
    m2.metric("Posisi X (Meter)", f"{data['x']:.2f} m")
    m3.metric("Posisi Y (Meter)", f"{data['y']:.2f} m")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📍 Jalur Robot di Kelas")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[data['x']], y=[data['y']], mode='markers+text', 
                                 marker=dict(size=25, color='cyan', symbol='triangle-up'),
                                 text=["ROBOT"], textposition="top center"))
        fig.update_layout(xaxis=dict(range=[-3, 3], title="Samping"), yaxis=dict(range=[-1, 5], title="Depan"), 
                          height=450, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("⚙️ Speed Motor")
        motor_df = pd.DataFrame({'RPM': [data['m1'], data['m2'], data['m3'], data['m4']]}, index=['M1', 'M2', 'M3', 'M4'])
        st.bar_chart(motor_df)

elif st.session_state.active_mode == "🎮 Manual Control":
    # --- UI MANUAL DENGAN CENTERING ---
    st.subheader("🎮 Nexus Remote (8-Direction Omni)")
    
    # Membuat layout centering
    _, center_col, _ = st.columns([0.5, 2, 0.5])
    
    with center_col:
        # Baris 1
        r1c1, r1c2, r1c3 = st.columns(3)
        if r1c1.button("↖️"): st.session_state.last_command = "DIAGONAL_NW"
        if r1c2.button("⬆️ MAJU"): st.session_state.last_command = "FORWARD"
        if r1c3.button("↗️"): st.session_state.last_command = "DIAGONAL_NE"

        # Baris 2
        r2c1, r2c2, r2c3 = st.columns(3)
        if r2c1.button("⬅️ KIRI"): st.session_state.last_command = "STRAFE_LEFT"
        if r2c2.button("🛑 STOP", type="primary"): st.session_state.last_command = "STOP"
        if r2c3.button("➡️ KANAN"): st.session_state.last_command = "STRAFE_RIGHT"

        # Baris 3
        r3c1, r3c2, r3c3 = st.columns(3)
        if r3c1.button("↙️"): st.session_state.last_command = "DIAGONAL_SW"
        if r3c2.button("⬇️ MUNDUR"): st.session_state.last_command = "BACKWARD"
        if r3c3.button("↘️"): st.session_state.last_command = "DIAGONAL_SE"

        st.divider()
        st.markdown(f"<div class='command-text'>SIGNAL: {st.session_state.last_command}</div>", unsafe_allow_html=True)

elif st.session_state.active_mode == "🤖 Auto Mode":
    # --- UI AUTO ---
    st.subheader("Autonomous Mission")
    auto_toggle = st.toggle("AKTIFKAN NAVIGASI OTOMATIS")
    
    if auto_toggle:
        st.success("Robot sedang menjalankan algoritma otomatis...")
        st.info("Memproses data IMU & Encoder untuk koreksi jalur.")
    else:
        st.warning("Sistem otomatis dalam keadaan STANDBY.")

# Footer Stabilitas IMU
st.divider()
st.caption(f"Stability Monitor | Pitch: {data['pitch']:.2f}° | Roll: {data['roll']:.2f}° | System Time: {time.strftime('%H:%M:%S')}")

# Auto Refresh
time.sleep(0.5)
st.rerun()
