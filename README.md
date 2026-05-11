# 🤖 Nexus Omniwheel 4WD Monitoring Dashboard
> **Real-time Telemetry & Kinematics Visualization for Omnidirectional Robot**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Polibatam](https://img.shields.io/badge/Campus-Politeknik%20Negeri%20Batam-blue)](https://www.polibatam.ac.id/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Proyek ini adalah sistem monitoring berbasis web untuk robot **Nexus Omniwheel 4 Roda** dengan konfigurasi **45° (X-Configuration)**. Dashboard ini memadukan data sensor IMU dan Encoder untuk memastikan stabilitas dan akurasi navigasi robot.

---

## 🚀 Fitur Utama
* **Live Orientation Gauge:** Visualisasi arah hadap (*heading*) robot secara real-time menggunakan sensor IMU.
* **Motor Sync Analysis:** Grafik perbandingan RPM ke-4 motor untuk mendeteksi ketidakseimbangan mekanis.
* **Field-Oriented Tracking:** Estimasi posisi robot (X, Y) di lapangan menggunakan perhitungan Odometri.
* **Stability Monitor:** Memantau kemiringan (*pitch/roll*) untuk mencegah robot terbalik pada kecepatan tinggi.

## 🛠️ Arsitektur Sistem
Dashboard dibangun menggunakan **Streamlit** (Python) sebagai interface utama. Aliran data dirancang sebagai berikut:
1.  **Robot Hardware:** Arduino/ESP32 membaca Encoder & IMU.
2.  **Communication:** Data dikirim via MQTT atau Serial.
3.  **Processing:** Dashboard menghitung kinematika 45° dan menampilkan visualisasi.

## 📐 Konfigurasi Roda (45°)
Robot menggunakan konfigurasi roda menyilang (X-Config). Kecepatan masing-masing roda ($V_1, V_2, V_3, V_4$) dihitung berdasarkan target kecepatan $V_x, V_y,$ dan kecepatan sudut $\omega$:



## 👨‍💻 Tim Pengembang
* **Apriyana Putra** - *Lead Developer*
* **Prodi Teknik Robotika** - *Politeknik Negeri Batam*

---
*Penelitian ini didorong oleh semangat inovasi di bidang Mobile Robotika.*

