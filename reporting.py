import streamlit as st
import google.generativeai as genai
import pandas as pd
import time
from datetime import datetime

# 1. Konfigurasi Halaman (Tampilan Wide & Modern)
st.set_page_config(page_title="GGova Report Pro", layout="wide")

st.markdown("""
    <style>
    .stCodeBlock { border-left: 5px solid #60a5fa !important; }
    .stExpander { border: 1px solid #e2e8f0; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inisialisasi History
if 'history' not in st.session_state:
    st.session_state['history'] = []

# 3. Setup Gemini 2.0 Flash
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# 4. Fungsi Load Data CSV (Database Materi)
@st.cache_data
def load_all_materi():
    try:
        df = pd.read_csv("Materi_gabungan.csv")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df_materi = load_all_materi()

def get_list_materi(level_pilihan):
    mask = df_materi['sheet_name'].str.contains(level_pilihan, case=False, na=False)
    df_filtered = df_materi[mask]
    potential_cols = ['Nama Materi', 'Nama Materi.1', 'Materi']
    list_res = []
    for col in potential_cols:
        if col in df_filtered.columns:
            list_res.extend(df_filtered[col].dropna().unique().tolist())
    return sorted(list(set([m for m in list_res if str(m).strip()])))

# =========================================================
# SIDEBAR (Control & History)
# =========================================================
with st.sidebar:
    st.title("📜 Riwayat Laporan")
    if st.button("🗑️ Hapus Riwayat", use_container_width=True):
        st.session_state['history'] = []
        st.rerun()
    
    for item in reversed(st.session_state['history']):
        with st.expander(f"📌 {item['nama']}"):
            st.caption(item['waktu'])
            st.write(item['laporan'])
    
    st.divider()
    num_students = st.number_input("Jumlah Murid", 1, 30, 1)

# =========================================================
# UI UTAMA (Input Data Murid)
# =========================================================
st.markdown("<h1 style='text-align: center; color: #60a5fa;'>🤖 GGova AI Reporting</h1>", unsafe_allow_html=True)

all_student_data = []

for i in range(num_students):
    with st.expander(f"👤 DATA MURID #{i+1}", expanded=(i == 0)):
        c1, c2, c3 = st.columns([2, 3, 2])
        
        with c1:
            nama = st.text_input("Nama Murid", key=f"n_{i}")
            kat = st.selectbox("Kategori", ["Coding", "Robotic"], key=f"k_{i}")
            level_opt = ["FWP 1.0", "FWP 2.0", "Robot Explorer 2.0"] if kat == "Robotic" else ["Coding Scratch", "Coding Picto", "Coding Construct", "Coding Roblox"]
            lvl = st.selectbox("Level", level_opt, key=f"l_{i}")
            lang = st.selectbox("Bahasa", ["Indonesia", "English"], key=f"lang_{i}")

        with c2:
            jml_p = st.selectbox("Jumlah Project", [1, 2, 3], key=f"jp_{i}")
            daftar_materi = get_list_materi(lvl)
            
            m1 = st.selectbox(f"Materi 1", daftar_materi, key=f"m1_{i}")
            s1 = st.radio(f"Status P1", ["Selesai", "Lanjut"], key=f"s1_{i}", horizontal=True)
            
            m2 = st.selectbox(f"Materi 2", daftar_materi, key=f"m2_{i}") if jml_p >= 2 else ""
            s2 = st.radio(f"Status P2", ["Selesai", "Lanjut"], key=f"s2_{i}", horizontal=True) if jml_p >= 2 else ""

        with c3:
            obs = st.text_input("Sikap (Sangat Mandiri, Fokus...)", key=f"obs_{i}")
            det = st.text_input("Detail Teknis (Paham Tilt Sensor...)", key=f"det_{i}")
            style = st.selectbox("Gaya", ["Ceria", "Formal", "Santai"], key=f"sty_{i}")

        all_student_data.append({
            "nama": nama, "m1": m1, "s1": s1, "m2": m2, "s2": s2,
            "obs": obs, "det": det, "style": style, "lang": lang
        })

# =========================================================
# EKSEKUSI GENERATE (Dengan Proteksi Anti-Error)
# =========================================================
if st.button("🚀 GENERATE SEMUA LAPORAN", use_container_width=True):
    active_students = [d for d in all_student_data if d["nama"]]
    
    for idx, data in enumerate(active_students):
        # Proteksi: Jeda 13 detik agar tidak kena Limit 5 RPM (berdasarkan dashboardmu)
        if idx > 0:
            with st.spinner(f"Menunggu jeda aman API agar tidak error..."):
                time.sleep(13)

        # Logika Note Otomatis
        note_text = "Good job! Pertahankan semangatnya." if data["s1"] == "Selesai" else "Semangat terus! Kita lanjut pertemuan depan."
        
        prompt = f"""
        Buat laporan 1 kalimat bercerita untuk orang tua murid.
        Nama: {data['nama']}, Project: {data['m1']} ({data['s1']}), Sikap: {data['obs']}, Teknis: {data['det']}.
        Gaya: {data['style']}, Bahasa: {data['lang']}.
        Pola: [Nama] hari ini hebat sekali mengerjakan [Project] dengan [Sikap] dan berhasil memahami [Teknis].
        """

        try:
            res = model.generate_content(prompt).text.strip()
            st.session_state['history'].append({"nama": data["nama"], "laporan": res, "waktu": datetime.now().strftime("%H:%M")})
            
            st.subheader(f"✅ Hasil: {data['nama']}")
            st.markdown("**Laporan untuk Orang Tua:**")
            st.code(res, language="text") # KLIK UNTUK SALIN
            st.markdown("**Note Tambahan:**")
            st.code(note_text, language="text")
            st.divider()
        except Exception as e:
            st.error(f"Error pada {data['nama']}: {e}. Coba lagi nanti atau ganti API Key.")
