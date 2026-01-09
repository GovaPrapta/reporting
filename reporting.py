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
.small-muted {
    color: #94a3b8;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("<div class='main-title'>🤖 AI Assistant – Reporting Anak</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Generator laporan perkembangan proyek anak (1 paragraf, variatif, 24 jam history)</div>", unsafe_allow_html=True)

# =========================================================
# INIT HISTORY (24 JAM)
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []

def _prune_history():
    now = datetime.now()
    st.session_state.history = [
        h for h in st.session_state.history
        if now - h["time"] <= timedelta(days=1)
    ]

def save_history(text, meta: dict):
    now = datetime.now()
    st.session_state.history.append({"time": now, "text": text, "meta": meta})
    _prune_history()

_prune_history()

# =========================================================
# CORE: GENERATE REPORT (1 PARAGRAF + VARIASI)
# =========================================================
def generate_project_report(nama: str, jenis: str, status: str, level: str, progres: str, bahasa: str) -> str:
    n = nama.strip().title()
    j = jenis.lower()

    progres_id = {
        "Melanjutkan Project": "melanjutkan project sebelumnya",
        "Project Baru": "mengerjakan project baru"
    }
    progres_en = {
        "Melanjutkan Project": "continued the previous project",
        "Project Baru": "worked on a new project"
    }

    # =============================
    # PARAGRAF 1 (INDONESIA)
    # =============================
    id_paragraph_1 = {
        "Baik": [
            "{n} {p} pada project {j} dengan performa yang sangat baik. {n} bekerja secara mandiri, fokus selama proses pengerjaan, serta menunjukkan pemahaman konsep yang kuat sehingga project dapat berjalan dengan lancar.",
            "{n} {p} pada project {j} dengan hasil yang sangat memuaskan. Kemandirian dan fokus {n} terlihat konsisten, dan {n} mampu menerapkan konsep dengan tepat saat menjalankan project."
        ],
        "Cukup": [
            "{n} {p} pada project {j} dengan hasil yang cukup baik. Selama pengerjaan, {n} masih memerlukan arahan ringan dan penguatan fokus, namun sudah mampu mengikuti alur project dengan cukup konsisten.",
            "{n} {p} pada project {j} dengan capaian yang cukup memadai. Ketelitian {n} masih perlu ditingkatkan, tetapi {n} tetap menunjukkan usaha dan kemauan belajar yang positif."
        ],
        "Perlu Bimbingan": [
            "{n} {p} pada project {j}, namun masih mengalami beberapa kendala. Fokus dan pemahaman konsep {n} belum stabil sehingga diperlukan pendampingan lanjutan.",
            "{n} {p} pada project {j}, tetapi pengerjaan belum optimal karena konsentrasi {n} mudah teralihkan dan masih diperlukan penguatan konsep dasar."
        ]
    }

    # =============================
    # PARAGRAF 2 (INDONESIA – ALTERNATIF)
    # =============================
    id_paragraph_2 = {
        "Baik": [
            "Dalam kegiatan ini, {n} menunjukkan kinerja yang sangat positif saat {p} pada project {j}. Kemandirian dan konsistensi fokus {n} menjadi faktor utama keberhasilan pengerjaan project.",
            "Selama {p} pada project {j}, {n} mampu bekerja secara terstruktur dan menjaga fokus dengan baik. Hal ini membuat proses pengerjaan berjalan lancar dan hasilnya sesuai tujuan pembelajaran."
        ],
        "Cukup": [
            "Saat {p} pada project {j}, {n} menunjukkan pemahaman dasar yang cukup baik. Meskipun konsistensi dan ketelitian masih perlu ditingkatkan, {n} tetap menunjukkan kemauan belajar yang baik.",
            "Dalam proses {p} pada project {j}, {n} sudah dapat mengikuti langkah-langkah utama, namun masih membutuhkan arahan ringan agar pengerjaan lebih rapi dan konsisten."
        ],
        "Perlu Bimbingan": [
            "Dalam proses {p} pada project {j}, {n} masih membutuhkan bimbingan lebih lanjut karena fokus dan pemahaman konsep belum berkembang secara optimal.",
            "Saat {p} pada project {j}, {n} masih memerlukan pendampingan untuk menjaga konsentrasi dan memperkuat pemahaman agar pengerjaan dapat lebih terarah."
        ]
    }

    # =============================
    # CATATAN STATUS (INDONESIA)
    # =============================
    id_status_suffix = {
        "Selesai": [
            "Project dinyatakan selesai dan dapat diuji dengan baik.",
            "Pengerjaan selesai dan hasilnya sesuai dengan target.",
            "Project selesai dan berjalan sesuai yang diharapkan."
        ],
        "Tidak Selesai": [
            "Project belum selesai karena masih ada bagian yang perlu diperbaiki.",
            "Pengerjaan belum tuntas dan masih memerlukan perbaikan pada beberapa bagian.",
            "Project belum dapat dijalankan sepenuhnya karena masih terdapat kesalahan."
        ]
    }

    # =============================
    # ENGLISH (1 PARAGRAPH)
    # =============================
    en_paragraph = {
        "Baik": [
            "{n} {p} in the {j} project with excellent performance. {n} worked independently, maintained strong focus, and demonstrated solid understanding of the applied concepts.",
            "During the session, {n} {p} in the {j} project and showed excellent independence and consistent focus."
        ],
        "Cukup": [
            "{n} {p} in the {j} project with fairly good results. Some guidance was still required, particularly to maintain focus and consistency.",
            "{n} {p} in the {j} project and showed basic understanding, although further practice is needed for better consistency."
        ],
        "Perlu Bimbingan": [
            "{n} {p} in the {j} project but faced several challenges. Focus and conceptual understanding still need further support.",
            "{n} {p} in the {j} project; however, additional guidance is needed to improve focus and understanding."
        ]
    }

    en_status_suffix = {
        "Selesai": [
            "The project was completed successfully and tested well.",
            "The task was completed and met the expected goal.",
            "The project was finished and ran as intended."
        ],
        "Tidak Selesai": [
            "The project was not completed yet due to remaining issues.",
            "The task is still unfinished and requires further correction.",
            "The project could not run fully because some errors remain."
        ]
    }

    if bahasa == "Indonesia":
        p = progres_id[progres]
        paragraf = random.choice(id_paragraph_1[level] + id_paragraph_2[level]).format(n=n, j=j, p=p)
        status_suffix = random.choice(id_status_suffix[status])
        return f"{paragraf} {status_suffix}"
    else:
        p = progres_en[progres]
        jj = "robotics" if j == "robotic" else "coding"
        paragraf = random.choice(en_paragraph[level]).format(n=n, j=jj, p=p)
        status_suffix = random.choice(en_status_suffix[status])
        return f"{paragraf} {status_suffix}"

# =========================================================
# INPUT FORM
# =========================================================
st.subheader("📝 Input Laporan Proyek")
st.markdown("<div class='small-muted'>Output laporan 1 paragraf (singkat), variatif, dan tersimpan 24 jam.</div>", unsafe_allow_html=True)

nama = st.text_input("Nama Anak", placeholder="Contoh: Dista")
jenis = st.selectbox("Jenis Project", ["Coding", "Robotic"])
progres = st.radio("Jenis Kegiatan", ["Melanjutkan Project", "Project Baru"], horizontal=True)
status = st.radio("Status Project", ["Selesai", "Tidak Selesai"], horizontal=True)
level = st.selectbox("Level Performa", ["Baik", "Cukup", "Perlu Bimbingan"])
bahasa = st.selectbox("Bahasa Laporan", ["Indonesia", "English"])

# =========================================================
# GENERATE REPORT
# =========================================================
colA, colB = st.columns([1, 1])
with colA:
    gen = st.button("🚀 Buat Laporan", use_container_width=True)
with colB:
    regen = st.button("🔁 Buat Variasi Baru", use_container_width=True)

if gen or regen:
    if not nama.strip():
        st.warning("Nama anak wajib diisi.")
    else:
        laporan = generate_project_report(nama, jenis, status, level, progres, bahasa)
        meta = {
            "nama": nama.strip().title(),
            "jenis": jenis,
            "progres": progres,
            "status": status,
            "level": level,
            "bahasa": bahasa
        }
        save_history(laporan, meta)

        st.subheader("📄 Hasil Laporan AI")
        st.text_area("", laporan, height=180)

# =========================================================
# HISTORY (24 JAM)
# =========================================================
with st.expander("📜 Riwayat Laporan (24 Jam Terakhir)"):
    _prune_history()
    if not st.session_state.history:
        st.write("Belum ada laporan.")
    else:
        for h in reversed(st.session_state.history):
            t = h["time"].strftime("%d-%m-%Y %H:%M")
            meta = h.get("meta", {})
            meta_line = f"{meta.get('jenis','-')} | {meta.get('progres','-')} | {meta.get('status','-')} | {meta.get('level','-')} | {meta.get('bahasa','-')}"
            st.markdown(f"**{t}** — {meta_line}")
            st.text(h["text"])
            st.divider()
