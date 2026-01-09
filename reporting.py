import streamlit as st
import random
from datetime import datetime, timedelta

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="AI Assistant – Reporting Anak",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617);
    color: #f8fafc;
}
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    background: linear-gradient(90deg, #60a5fa, #a855f7, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub-title {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("<div class='main-title'>🤖 AI Assistant – Reporting Anak</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Generator laporan perkembangan proyek anak (AI Rule-Based)</div>", unsafe_allow_html=True)

# =========================================================
# INIT HISTORY (24 JAM)
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []

def save_history(text):
    now = datetime.now()
    st.session_state.history.append({"time": now, "text": text})
    st.session_state.history = [
        h for h in st.session_state.history
        if now - h["time"] <= timedelta(days=1)
    ]

# =========================================================
# AI REPORTING FUNCTION (PANJANG & VARIATIF)
# =========================================================
def generate_project_report(nama, jenis, status, level, progres, bahasa):
    nama = nama.strip().title()
    jenis = jenis.lower()

    # -------------------------
    # KALIMAT PROGRES PROJECT
    # -------------------------
    progres_id = {
        "Melanjutkan Project": "melanjutkan project sebelumnya",
        "Project Baru": "mengerjakan project baru"
    }

    progres_en = {
        "Melanjutkan Project": "continued the previous project",
        "Project Baru": "worked on a new project"
    }

    # -------------------------
    # DESKRIPSI PANJANG (ID)
    # -------------------------
    deskripsi_id = {
        "Baik": [
            "{n} {p} pada bidang {j} dengan performa yang sangat baik. Selama proses pengerjaan, {n} menunjukkan sikap mandiri, fokus yang stabil, serta mampu mengikuti instruksi dengan sangat baik. Selain itu, {n} juga aktif mencoba memahami konsep yang digunakan dan mampu menjalankan project dengan lancar tanpa kendala berarti.",
            "Dalam kegiatan {p}, {n} memperlihatkan kemampuan yang sangat baik pada project {j}. {n} dapat bekerja secara mandiri, menjaga konsentrasi dengan baik, serta menunjukkan pemahaman yang matang terhadap konsep yang diterapkan dalam project."
        ],
        "Cukup": [
            "{n} {p} pada project {j} dengan hasil yang cukup baik. Selama pengerjaan, {n} masih memerlukan arahan ringan dan penguatan fokus pada beberapa bagian, namun secara umum sudah mampu mengikuti alur pengerjaan dengan cukup baik.",
            "Saat {p} pada project {j}, {n} menunjukkan pemahaman dasar yang cukup baik. Meskipun masih terdapat beberapa kekurangan dalam ketelitian dan fokus, {n} tetap menunjukkan usaha dan kemauan belajar yang positif."
        ],
        "Perlu Bimbingan": [
            "{n} {p} pada project {j}, namun masih mengalami beberapa kendala. Fokus {n} belum stabil selama proses pengerjaan dan masih diperlukan pendampingan untuk memahami konsep dasar yang digunakan.",
            "Dalam proses {p} pada project {j}, {n} masih membutuhkan bimbingan lebih lanjut. Beberapa kesalahan masih muncul dan perlu adanya penguatan pemahaman serta peningkatan konsentrasi."
        ]
    }

    # -------------------------
    # DESKRIPSI PANJANG (EN)
    # -------------------------
    deskripsi_en = {
        "Baik": [
            "{n} {p} in the {j} project with excellent performance. Throughout the activity, {n} demonstrated strong independence, consistent focus, and a solid understanding of the concepts applied in the project.",
            "While {p} in the {j} project, {n} showed very good performance and was able to complete tasks independently with minimal guidance."
        ],
        "Cukup": [
            "{n} {p} in the {j} project with fairly good results. Some guidance was still required, particularly to maintain focus and accuracy during the process.",
            "During the activity, {n} demonstrated basic understanding while {p} in the {j} project, although further practice is still needed."
        ],
        "Perlu Bimbingan": [
            "{n} {p} in the {j} project but faced several challenges. Focus was inconsistent and additional guidance is required to strengthen understanding.",
            "While {p} in the {j} project, {n} required close assistance and further support to complete the tasks effectively."
        ]
    }

    note_id = {
        "Baik": "Anak siap untuk melanjutkan ke tahap pembelajaran atau project berikutnya. Tetap semangat dan pertahankan kinerja yang baik.",
        "Cukup": "Disarankan untuk melakukan latihan lanjutan agar pemahaman dan fokus anak semakin meningkat.",
        "Perlu Bimbingan": "Perlu pendampingan lebih intensif serta penguatan konsep pada pertemuan selanjutnya."
    }

    note_en = {
        "Baik": "The student is ready to move on to the next project or learning stage. Keep up the good work.",
        "Cukup": "Further practice is recommended to improve understanding and focus.",
        "Perlu Bimbingan": "Additional guidance and reinforcement are recommended in the next session."
    }

    # -------------------------
    # PILIH BAHASA & TEMPLATE
    # -------------------------
    if bahasa == "Indonesia":
        kalimat = random.choice(deskripsi_id[level])
        note = note_id[level]
        progres_text = progres_id[progres]
    else:
        kalimat = random.choice(deskripsi_en[level])
        note = note_en[level]
        progres_text = progres_en[progres]

    return f"""
{nama}

{kalimat.format(n=nama, j=jenis, p=progres_text)}

Note: {note}
""".strip()

# =========================================================
# INPUT FORM
# =========================================================
st.subheader("📝 Input Laporan Proyek")

nama = st.text_input("Nama Anak")
jenis = st.selectbox("Jenis Project", ["Coding", "Robotic"])
progres = st.radio("Jenis Kegiatan", ["Melanjutkan Project", "Project Baru"])
status = st.radio("Status Project", ["Selesai", "Tidak Selesai"])
level = st.selectbox("Level Performa", ["Baik", "Cukup", "Perlu Bimbingan"])
bahasa = st.selectbox("Bahasa Laporan", ["Indonesia", "English"])

# =========================================================
# GENERATE REPORT
# =========================================================
if st.button("🚀 Buat Laporan"):
    if not nama:
        st.warning("Nama anak wajib diisi.")
    else:
        laporan = generate_project_report(
            nama, jenis, status, level, progres, bahasa
        )
        save_history(laporan)

        st.subheader("📄 Hasil Laporan AI")
        st.text_area("", laporan, height=320)

# =========================================================
# HISTORY (24 JAM)
# =========================================================
with st.expander("📜 Riwayat Laporan (24 Jam Terakhir)"):
    if not st.session_state.history:
        st.write("Belum ada laporan.")
    else:
        for h in reversed(st.session_state.history):
            st.markdown(f"**{h['time'].strftime('%d-%m-%Y %H:%M')}**")
            st.text(h["text"])
            st.divider()
