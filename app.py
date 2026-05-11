import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Nexus Omni 4WD Control", layout="wide")

# Custom CSS untuk tema gelap yang menarik
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; color: white; }
    .stButton>button:hover { background-color: #ff4b4b; border: 1px solid white; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZING SESSION STATE ---
# Digunakan agar mode tidak berubah sebelum dikonfirmasi
if 'active_mode' not in st.session_state:
    st.session_state.active_mode = "📊 Monitoring"
if 'last_command' not in st.session_state:
    st.session_state.last_command = "STOP"

# --- SIDEBAR: KONTROL MODE & KONFIRMASI ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/id/c/c9/Logo_Polibatam.png", width=100)
st.sidebar.title("Robot Control Panel")

# Pilihan Mode (Belum Aktif sebelum dikonfirmasi)
selected_mode = st.sidebar.radio(
    "Pilih Mode Operasi:",
    ["📊 Monitoring", "🎮 Manual Control", "🤖 Auto Mode"],
    index=0
)

# Tombol Konfirmasi
st.sidebar.divider()
if st.sidebar.button("✅ KONFIRMASI MODE", type="primary"):
    st.session_state.active_mode = selected_mode
    st.sidebar.success(f"Mode {selected_mode} Aktif!")

st.sidebar.info(f"Mode Saat Ini: **{st.session_state.active_mode}**")

# --- FUNGSI SIMULASI DATA (KINEMATIKA & IMU) ---
def get_telemetry():
    return {
        "yaw": np.random.uniform(0, 360),
        "pitch": np.random.uniform(-2, 2),
        "roll": np.random.uniform(-2, 2),
        "m1": np.random.randint(90, 110),
        "m2": np.random.randint(90, 110),
        "m3": np.random.randint(90, 110),
        "m4": np.random.randint(90, 110),
        "x": np.random.uniform(-2, 2),
        "y": np.random.uniform(0, 5)
    }

data = get_telemetry()

# --- LOGIKA TAMPILAN UTAMA ---

st.title(f"Robot Operation: {st.session_state.active_mode}")
st.write("Apriyana Putra - Teknik Robotika Politeknik Negeri Batam")

if st.session_state.active_mode == "📊 Monitoring":
    # --- TAMPILAN MONITORING (KINEMATIKA) ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Heading (Yaw)", f"{data['yaw']:.1f}°")
    col2.metric("Posisi X", f"{data['x']:.2f} m")
    col3.metric("Posisi Y", f"{data['y']:.2f} m")

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📍 Indoor Path Tracking")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[data['x']], y=[data['y']], mode='markers+text', 
                                 marker=dict(size=20, color='red', symbol='triangle-up')))
        fig.update_layout(xaxis=dict(range=[-3, 3]), yaxis=dict(range=[0, 6]), height=400, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("⚙️ Wheel Synchronization")
        motor_df = pd.DataFrame({'RPM': [data['m1'], data['m2'], data['m3'], data['m4']]}, index=['M1', 'M2', 'M3', 'M4'])
        st.bar_chart(motor_df)

elif st.session_state.active_mode == "🎮 Manual Control":
    # --- TAMPILAN MANUAL (REMOTE) ---
    st.subheader("Remote Control - Nexus 45° Omni")
    st.write("Klik tombol untuk mengirim perintah pergerakan ke robot.")
    
    # Layout Remote Control 3x3
    row1_1, row1_2, row1_3 = st.columns(3)
    if row1_1.button("↖️"): st.session_state.last_command = "MAJU-KIRI"
    if row1_2.button("⬆️ MAJU"): st.session_state.last_command = "MAJU"
    if row1_3.button("↗️"): st.session_state.last_command = "MAJU-KANAN"

    row2_1, row2_2, row2_3 = st.columns(3)
    if row2_1.button("⬅️ KIRI"): st.session_state.last_command = "GESER KIRI"
    if row2_2.button("🛑 STOP", type="primary"): st.session_state.last_command = "STOP"
    if row2_3.button("➡️ KANAN"): st.session_state.last_command = "GESER KANAN"

    row3_1, row3_2, row3_3 = st.columns(3)
    if row3_1.button("↙️"): st.session_state.last_command = "MUNDUR-KIRI"
    if row3_2.button("⬇️ MUNDUR"): st.session_state.last_command = "MUNDUR"
    if row3_3.button("↘️"): st.session_state.last_command = "MUNDUR-KANAN"

    st.divider()
    st.info(f"Sinyal Terkirim: **{st.session_state.last_command}**")

elif st.session_state.active_mode == "🤖 Auto Mode":
    # --- TAMPILAN AUTO (ON/OFF) ---
    st.subheader("Autonomous Navigation")
    st.write("Robot akan berjalan berdasarkan algoritma deteksi rintangan / fuzzy logic.")
    
    auto_status = st.toggle("AKTIFKAN SISTEM OTOMATIS")
    
    if auto_status:
        st.success("STATUS: Robot sedang berjalan otomatis...")
        st.write("Sistem sedang memproses data sensor untuk navigasi kelas.")
    else:
        st.error("STATUS: Sistem Otomatis Mati.")

# --- FOOTER DATA ---
with st.expander("Sensor Detail (IMU Stability)"):
    st.write(f"Pitch: {data['pitch']:.2f}° | Roll: {data['roll']:.2f}°")

# Auto-refresh agar data terlihat hidup
time.sleep(0.5)
st.rerun()
