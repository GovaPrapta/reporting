import streamlit as st
import google.generativeai as genai
import os

# =========================================================
# KONFIGURASI API GEMINI
# =========================================================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    st.error("API Key tidak ditemukan. Pastikan sudah setting di Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') # Gunakan model stabil

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(page_title="AI Reporting – Progres & Note", page_icon="📝", layout="centered")

st.markdown("""
<style>
.stApp { background: #0f172a; color: #f8fafc; }
.main-title { text-align: center; font-size: 32px; font-weight: 800; color: #60a5fa; }
.report-box { background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #60a5fa; margin-bottom: 20px;}
.note-box { background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #f59e0b; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🤖 AI Reporting - by GOVA </div>", unsafe_allow_html=True)

# =========================================================
# FUNGSI GENERATE
# =========================================================
def generate_report_ai(nama, jenis, alat_level, materi, status, level_performa, progres, style):
    if status == "Selesai":
        note_text = "Bisa lanjut ke project berikutnya."
    else:
        note_text = "Bisa dilanjutkan di pertemuan selanjutnya." if jenis == "Coding" else "Kita coba di pertemuan selanjutnya."

    prompt = f"""
    Bertindaklah sebagai instruktur {jenis}. Buat laporan singkat satu paragraf.
    Ikuti pola ini:
    - Selesai: "Hari ini {nama} mampu mengerjakan projectnya dengan baik dan mandiri. Fokus dalam mengerjakan projectnya dan hasilnya sudah sesuai dengan instruksi yang diberikan oleh teacher."
    - Belum Selesai: "Hari ini {nama} {progres} {materi}. Dimana {nama} telah [sebutkan progres teknis] namun masih [sebutkan kendala teknis]."
    
    Akhiri dengan kalimat motivasi (Tetap semangat/Jangan menyerah).
    Data: Nama {nama}, Materi {materi}, Status {status}, Performa {level_performa}, Alat {alat_level}.
    """

    try:
        response = model.generate_content(prompt)
        return response.text, note_text
    except Exception as e:
        return f"Error: {str(e)}", ""

# =========================================================
# INPUT FORM
# =========================================================
with st.container():
    nama = st.text_input("Nama Anak", placeholder="Contoh: Gungde")
    
    col1, col2 = st.columns(2)
    with col1:
        jenis = st.selectbox("Jenis Kelas", ["Coding", "Robotic"])
        if jenis == "Robotic":
            alat_level = st.selectbox("Level Robotic", ["Robotic Explorer 1.0", "Robotic Explorer 2.0", "Arduino"])
        else:
            alat_level = st.selectbox("Platform Coding", ["Scratch", "Construct", "Roblox"])
        
        materi = st.text_input("Materi Hari Ini")
        progres_pilihan = st.radio("Jenis Kegiatan", ["melanjutkan project", "membuat project baru"])

    with col2:
        status = st.radio("Status Project", ["Selesai", "Tidak Selesai"])
        level_performa = st.selectbox("Level Performa", ["Baik", "Cukup", "Perlu Bimbingan"])
        style = st.selectbox("Style Bahasa", ["Formal", "Santai", "Motivasional"])

# =========================================================
# PROSES GENERATE
# =========================================================
if st.button("🚀 Generate Gak Nih!!", use_container_width=True):
    if not nama.strip() or not materi.strip():
        st.warning("Nama dan Materi harus diisi!")
    else:
        with st.spinner('Menyusun data...'):
            laporan_utama, catatan_instruksi = generate_report_ai(
                nama, jenis, alat_level, materi, status, 
                level_performa, progres_pilihan, style
            )
            
            st.divider()
            st.markdown("### 📘 Pembelajaran Hari Ini")
            st.markdown(f"<div class='report-box'>{laporan_utama}</div>", unsafe_allow_html=True)
            
            st.markdown("### 📋 Note / Catatan")
            st.markdown(f"<div class='note-box'>{catatan_instruksi}</div>", unsafe_allow_html=True)
            

st.divider()
st.caption("© Govaa")




