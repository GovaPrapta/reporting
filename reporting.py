import streamlit as st
import google.generativeai as genai
import pandas as pd
import os
from datetime import datetime

# WAJIB: Perintah pertama Streamlit
st.set_page_config(page_title="Quick AI Reporting", layout="wide")

# =========================================================
# INISIALISASI SESSION STATE
# =========================================================
if 'history' not in st.session_state:
    st.session_state['history'] = []

# =========================================================
# KONFIGURASI API GEMINI
# =========================================================
# Ganti dengan API Key Anda atau masukkan di Streamlit Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    st.error("API Key tidak ditemukan. Pastikan sudah diatur di environment variable atau secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# =========================================================
# FUNGSI DATA
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
# SIDEBAR HISTORY
# =========================================================
st.sidebar.title("📜 History Laporan")
if st.sidebar.button("🗑️ Bersihkan History"):
    st.session_state['history'] = []

if st.session_state['history']:
    for item in reversed(st.session_state['history']):
        with st.sidebar.expander(f"📌 {item['nama']} ({item['waktu']})"):
            st.write(item['laporan'])
            st.caption(f"Note: {item['note']}")
else:
    st.sidebar.info("Belum ada riwayat.")

st.sidebar.divider()
num_students = st.sidebar.number_input("Jumlah Murid", min_value=1, max_value=30, value=1)

# =========================================================
# UI UTAMA
# =========================================================
st.markdown("<h2 style='text-align: center; color: #60a5fa;'>🤖 reporting AI Gova</h2>", unsafe_allow_html=True)

all_student_data = []

for i in range(num_students):
    with st.expander(f"👤 Data Murid #{i+1}", expanded=(i == 0)):
        c1, c2, c3 = st.columns([2, 2, 2])
        
        with c1:
            nama = st.text_input("Nama Murid", key=f"n_{i}")
            kategori = st.selectbox("Kategori", ["Coding", "Robotic"], key=f"k_{i}")
            level = st.selectbox("Level", ["FWP 1.0", "FWP 2.0", "Robot Explorer 2.0"] if kategori == "Robotic" else ["Coding Scratch", "Coding Picto", "Coding Construct", "Coding Roblox"], key=f"l_{i}")
            jml_p = st.selectbox("Jumlah Project", [1, 2, 3], key=f"jp_{i}")

        with c2:
            daftar_materi = get_list_materi(level)
            m1 = st.selectbox(f"Materi 1", daftar_materi, key=f"m1_{i}")
            s1 = st.radio(f"Status P1", ["Selesai", "Lanjut"], key=f"s1_{i}", horizontal=True)
            
            m2 = st.selectbox(f"Materi 2", daftar_materi, key=f"m2_{i}") if jml_p >= 2 else ""
            s2 = st.radio(f"Status P2", ["Selesai", "Lanjut"], key=f"s2_{i}", horizontal=True) if jml_p >= 2 else ""
            
            m3 = st.selectbox(f"Materi 3", daftar_materi, key=f"m3_{i}") if jml_p == 3 else ""
            s3 = st.radio(f"Status P3", ["Selesai", "Lanjut"], key=f"s3_{i}", horizontal=True) if jml_p == 3 else ""

        with c3:
            obs = st.text_input("Sikap (menguap, semangat, ceria...)", key=f"obs_{i}")
            det = st.text_input("Detail Teknis (nambah code, gear motor...)", key=f"det_{i}")
            style = st.selectbox("Gaya", ["Santai", "Formal", "Ceria"], key=f"sty_{i}")

        all_student_data.append({
            "nama": nama, "kat": kategori, "lvl": level, "jp": jml_p,
            "m1": m1, "s1": s1, "m2": m2, "s2": s2, "m3": m3, "s3": s3,
            "obs": obs, "det": det, "style": style
        })

# =========================================================
# PROSES GENERATE
# =========================================================
if st.button("🚀 Generate Semua Laporan", use_container_width=True):
    active_students = [d for d in all_student_data if d["nama"]]
    if not active_students:
        st.error("Mohon isi setidaknya satu nama murid!")
    else:
        st.divider()
        for data in active_students:
            # 1. Logika Note (Apresiasi + Instruksi)
            last_s = data["s1"] if data["jp"] == 1 else (data["s2"] if data["jp"] == 2 else data["s3"])
            if last_s == "Selesai":
                note_text = "Good job! Pertahankan semangatnya, bisa lanjut ke project selanjutnya ya."
            else:
                note_text = "Semangat terus! Kita ulang/lanjutkan lagi di pertemuan berikutnya ya."

            # 2. Persiapan Info Project (Menghindari Syntax Error f-string)
            p_list = [f"{data['m1']} ({data['s1']})"]
            if data["m2"]: p_list.append(f"{data['m2']} ({data['s2']})")
            if data["m3"]: p_list.append(f"{data['m3']} ({data['s3']})")
            project_summary = ", ".join(p_list)

            # 3. Prompt AI Singkat
            prompt = f"""
            Buat laporan belajar 1 kalimat (maksimal 2 kalimat pendek) untuk {data['nama']} (Kelas {data['kat']}).
            Project: {project_summary}.
            Observasi Sikap: {data['obs']}.
            Detail Teknis: {data['det']}.
            
            Pola: "Hari ini {data['nama']} membuat/melanjutkan... [fakta teknis] dan [fakta sikap]. [Penyemangat]."
            Gaya: {data['style']}. Bahasa: Indonesia.
            """

            with st.status(f"Proses {data['nama']}...") as s:
                try:
                    res = model.generate_content(prompt).text.strip()
                    st.session_state['history'].append({"nama": data["nama"], "laporan": res, "note": note_text, "waktu": datetime.now().strftime("%H:%M")})
                    
                    # Tampilan Hasil
                    st.subheader(f"👤 {data['nama']}")
                    
                    st.markdown("**Laporan:**")
                    st.code(res, language="text") # Klik pojok kanan untuk copy
                    
                    st.markdown("**Note:**")
                    st.code(note_text, language="text") # Klik pojok kanan untuk copy
                    
                    st.divider()
                    s.update(label=f"Laporan {data['nama']} Selesai!", state="complete")
                except Exception as e:
                    st.error(f"Gagal generate {data['nama']}: {e}")

