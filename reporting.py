import streamlit as st
import google.generativeai as genai
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="ggova report PRO", layout="wide")

# =========================================================
# KONFIGURASI DUAL API KEY
# =========================================================
api_keys = [
    st.secrets.get("GEMINI_API_KEY_1"),
    st.secrets.get("GEMINI_API_KEY_2")
]

# Fungsi untuk mencoba generate dengan API cadangan jika yang pertama gagal
def generate_with_fallback(prompt):
    for i, key in enumerate(api_keys):
        if not key: continue # Skip jika key kosong
        
        try:
            genai.configure(api_key=key)
            # Menggunakan model flash terbaru
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            if "429" in str(e):
                st.warning(f"API Key {i+1} limit/habis. Mencoba API Key berikutnya...")
                continue # Coba key selanjutnya
            else:
                return f"Error: {str(e)}"
    
    return "❌ Semua API Key kamu sudah mencapai limit harian (20/20). Coba lagi besok jam 7 pagi."

# =========================================================
# FUNGSI DATA CSV (Kembali ke semula)
# =========================================================
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
# SIDEBAR & INPUT (Kembali ke semula)
# =========================================================
st.sidebar.title("📜 History")
if st.sidebar.button("🗑️ Bersihkan History"):
    st.session_state['history'] = []

num_students = st.sidebar.number_input("Jumlah Murid", 1, 30, 1)

st.markdown("<h2 style='text-align: center; color: #60a5fa;'>🤖 ggova report v2.1</h2>", unsafe_allow_html=True)

all_student_data = []
for i in range(num_students):
    with st.expander(f"👤 Data Murid #{i+1}", expanded=(i == 0)):
        c1, c2, c3 = st.columns([2, 2, 2])
        with c1:
            nama = st.text_input("Nama Murid", key=f"n_{i}")
            kat = st.selectbox("Kategori", ["Coding", "Robotic"], key=f"k_{i}")
            lvl = st.selectbox("Level", ["FWP 1.0", "FWP 2.0", "Robot Explorer 2.0"] if kat == "Robotic" else ["Coding Scratch", "Coding Picto", "Coding Construct", "Coding Roblox"], key=f"l_{i}")
            lang = st.selectbox("Bahasa", ["Indonesia", "English"], key=f"lang_{i}")
        with c2:
            jml_p = st.selectbox("Jumlah Project", [1, 2, 3], key=f"jp_{i}")
            materi_list = get_list_materi(lvl)
            m1 = st.selectbox(f"Materi 1", materi_list, key=f"m1_{i}")
            s1 = st.radio(f"Status P1", ["Selesai", "Lanjut"], key=f"s1_{i}", horizontal=True)
        with c3:
            obs = st.text_input("Sikap", key=f"obs_{i}")
            det = st.text_input("Teknis", key=f"det_{i}")
            style = st.selectbox("Gaya", ["Ceria", "Formal", "Santai"], key=f"sty_{i}")
        
        all_student_data.append({"nama": nama, "lang": lang, "m1": m1, "s1": s1, "obs": obs, "det": det, "style": style})

# =========================================================
# PROSES GENERATE
# =========================================================
if st.button("🚀 Generate Semua Laporan"):
    active = [d for d in all_student_data if d["nama"]]
    for idx, data in enumerate(active):
        if idx > 0:
            time.sleep(13) # Jeda aman 5 RPM
        
        prompt = f"Buat laporan singkat 1-2 kalimat untuk {data['nama']} tentang project {data['m1']} ({data['s1']}). Sikap: {data['obs']}. Teknis: {data['det']}. Bahasa: {data['lang']}. Gaya: {data['style']}."
        
        with st.status(f"Memproses {data['nama']}..."):
            hasil = generate_with_fallback(prompt)
        
        st.subheader(f"✅ {data['nama']}")
        st.code(hasil, language="text")
        st.divider()
