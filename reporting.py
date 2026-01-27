import streamlit as st
import google.generativeai as genai
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="GGova Report 2.0", layout="wide")

# =========================================================
# KONFIGURASI API (GEMINI 2.0 FLASH)
# =========================================================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Pastikan nama model sesuai dengan rilisan terbaru Google
model = genai.GenerativeModel('gemini-2.0-flash')

# =========================================================
# FUNGSI GENERATE DENGAN AUTO-RETRY
# =========================================================
def generate_laporan_aman(prompt):
    max_retries = 3
    for i in range(max_retries):
        try:
            # Jeda wajib 12 detik antar murid (Karena jatah 5 RPM)
            time.sleep(12) 
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "429" in str(e):
                # Jika kena limit, tunggu 65 detik lalu coba lagi
                st.warning(f"Limit tercapai, menunggu 65 detik... (Percobaan {i+1})")
                time.sleep(65)
            else:
                return f"Error: {str(e)}"
    return "Gagal setelah beberapa kali mencoba karena kuota habis."

# =========================================================
# UI & INPUT (Singkat)
# =========================================================
st.sidebar.title("⚙️ Pengaturan")
num_students = st.sidebar.number_input("Jumlah Murid", 1, 30, 1)

all_data = []
for i in range(num_students):
    with st.expander(f"👤 Murid {i+1}", expanded=(i==0)):
        c1, c2 = st.columns(2)
        with c1:
            nama = st.text_input("Nama", key=f"n{i}")
            proj = st.text_input("Project (Selesai/Lanjut)", key=f"p{i}")
        with c2:
            obs = st.text_input("Sikap (Satu kata saja: Semangat/Fokus)", key=f"o{i}")
            det = st.text_input("Teknis (Satu kata saja: Sensor/Looping)", key=f"d{i}")
        all_data.append({"nama": nama, "proj": proj, "obs": obs, "det": det})

# =========================================================
# EKSEKUSI
# =========================================================
if st.button("🚀 Buat Laporan 1 Kalimat", use_container_width=True):
    for data in all_data:
        if data["nama"]:
            prompt = f"""
            Buat 1 kalimat laporan singkat untuk orang tua.
            Nama: {data['nama']}, Project: {data['proj']}, Sikap: {data['obs']}, Teknis: {data['det']}.
            Gabungkan jadi kalimat mengalir. Maksimal 20 kata.
            Contoh: "Hari ini {data['nama']} hebat sekali saat mengerjakan {data['proj']} karena sangat {data['obs']} memahami {data['det']}."
            """
            
            with st.status(f"Sedang memproses {data['nama']}..."):
                hasil = generate_laporan_aman(prompt)
                
            st.subheader(f"✅ {data['nama']}")
            st.code(hasil, language="text") # Tombol Copy otomatis
            st.divider()
