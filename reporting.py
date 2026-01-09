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
st.markdown(
    "<div class='sub-title'>Laporan 1 paragraf + catatan evaluasi (dengan jumlah project)</div>",
    unsafe_allow_html=True
)

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
# NOTE TEMPLATE
# =========================================================
NOTE_ID = {
    "Baik": [
        "Bisa lanjut ke project berikutnya. Pertahankan fokus dan kemandirian yang sudah baik.",
        "Siap melanjutkan ke tahap berikutnya. Semangat terus!",
        "Dapat melanjutkan ke project selanjutnya. Kerja bagus!"
    ],
    "Cukup": [
        "Perlu latihan lanjutan agar fokus dan ketelitian semakin meningkat.",
        "Disarankan penguatan latihan pada bagian yang masih kurang konsisten.",
        "Teruskan latihan agar hasil pengerjaan lebih rapi dan stabil."
    ],
    "Perlu Bimbingan": [
        "Perlu pendampingan lebih intensif dan penguatan konsep pada pertemuan berikutnya.",
        "Disarankan pengulangan materi dasar dengan pendampingan bertahap.",
        "Perlu peningkatan fokus dan pemahaman sebelum melanjutkan ke tahap berikutnya."
    ]
}

NOTE_EN = {
    "Baik": [
        "Ready to continue to the next project. Keep up the good work!",
        "The student can proceed to the next stage with confidence."
    ],
    "Cukup": [
        "Further practice is recommended to improve focus and consistency."
    ],
    "Perlu Bimbingan": [
        "More intensive guidance is recommended in the next session."
    ]
}

# =========================================================
# UTIL JUMLAH PROJECT
# =========================================================
def project_count_text(jumlah, bahasa):
    if bahasa == "Indonesia":
        return "satu project" if jumlah == 1 else f"{jumlah} project"
    else:
        return "one project" if jumlah == 1 else f"{jumlah} projects"

# =========================================================
# CORE: GENERATE REPORT
# =========================================================
def generate_project_report(nama, jenis, status, level, progres, bahasa, jumlah_project):
    n = nama.strip().title()
    j = jenis.lower()
    count_text = project_count_text(jumlah_project, bahasa)

    progres_id = {
        "Melanjutkan Project": "melanjutkan project sebelumnya",
        "Project Baru": "mengerjakan project baru"
    }
    progres_en = {
        "Melanjutkan Project": "continued the previous project",
        "Project Baru": "worked on a new project"
    }

    id_paragraph = {
        "Baik": [
            "{n} {p} dengan mengerjakan {c} pada bidang {j} dengan performa yang sangat baik. {n} bekerja secara mandiri, fokus selama proses pengerjaan, serta mampu menyelesaikan tugas dengan hasil yang memuaskan.",
            "Dalam sesi ini, {n} berhasil {p} dengan menyelesaikan {c} pada project {j}. Kemandirian dan konsistensi fokus {n} terlihat sangat baik."
        ],
        "Cukup": [
            "{n} {p} dengan mengerjakan {c} pada project {j} dengan hasil yang cukup baik. {n} masih memerlukan arahan ringan, namun sudah mampu mengikuti alur pengerjaan dengan cukup konsisten.",
            "Saat {p}, {n} mengerjakan {c} pada project {j} dan menunjukkan pemahaman dasar yang cukup baik meskipun konsistensi masih perlu ditingkatkan."
        ],
        "Perlu Bimbingan": [
            "{n} {p} dengan mengerjakan {c} pada project {j}, namun masih mengalami beberapa kendala. Fokus dan pemahaman konsep {n} belum stabil sehingga diperlukan pendampingan lanjutan.",
            "Dalam proses {p}, {n} mengerjakan {c} pada project {j} tetapi masih membutuhkan bimbingan agar pengerjaan lebih terarah."
        ]
    }

    en_paragraph = {
        "Baik": [
            "{n} {p} by completing {c} in the {j} field with excellent performance. {n} worked independently and maintained strong focus throughout the session."
        ],
        "Cukup": [
            "{n} {p} by working on {c} in the {j} project with fairly good results. Some guidance was still required to maintain focus."
        ],
        "Perlu Bimbingan": [
            "{n} {p} by working on {c} in the {j} project but faced several challenges and required additional guidance."
        ]
    }

    if bahasa == "Indonesia":
        p = progres_id[progres]
        return random.choice(id_paragraph[level]).format(
            n=n, p=p, c=count_text, j=j
        )
    else:
        p = progres_en[progres]
        jj = "robotics" if j == "robotic" else "coding"
        return random.choice(en_paragraph[level]).format(
            n=n, p=p, c=count_text, j=jj
        )

# =========================================================
# INPUT FORM
# =========================================================
st.subheader("📝 Input Laporan Proyek")
st.markdown("<div class='small-muted'>Laporan singkat 1 paragraf dengan jumlah project.</div>", unsafe_allow_html=True)

nama = st.text_input("Nama Anak", placeholder="Contoh: Dista")
jenis = st.selectbox("Jenis Project", ["Coding", "Robotic"])
jumlah_project = st.number_input("Jumlah Project yang Dikerjakan", min_value=1, max_value=10, value=1)
progres = st.radio("Jenis Kegiatan", ["Melanjutkan Project", "Project Baru"], horizontal=True)
status = st.radio("Status Project", ["Selesai", "Tidak Selesai"], horizontal=True)
level = st.selectbox("Level Performa", ["Baik", "Cukup", "Perlu Bimbingan"])
bahasa = st.selectbox("Bahasa Laporan", ["Indonesia", "English"])

# =========================================================
# GENERATE REPORT
# =========================================================
colA, colB = st.columns(2)
with colA:
    gen = st.button("🚀 Buat Laporan", use_container_width=True)
with colB:
    regen = st.button("🔁 Buat Variasi Baru", use_container_width=True)

if gen or regen:
    if not nama.strip():
        st.warning("Nama anak wajib diisi.")
    else:
        laporan = generate_project_report(
            nama, jenis, status, level, progres, bahasa, jumlah_project
        )

        meta = {
            "nama": nama.strip().title(),
            "jenis": jenis,
            "jumlah": jumlah_project,
            "progres": progres,
            "status": status,
            "level": level,
            "bahasa": bahasa
        }
        save_history(laporan, meta)

        st.subheader("📄 Hasil Laporan AI")
        st.text_area("", laporan, height=160)

        # NOTE
        if bahasa == "Indonesia":
            st.info(f"📝 **Catatan:** {random.choice(NOTE_ID[level])}")
        else:
            st.info(f"📝 **Note:** {random.choice(NOTE_EN[level])}")

# =========================================================
# HISTORY
# =========================================================
with st.expander("📜 Riwayat Laporan (24 Jam Terakhir)"):
    _prune_history()
    if not st.session_state.history:
        st.write("Belum ada laporan.")
    else:
        for h in reversed(st.session_state.history):
            t = h["time"].strftime("%d-%m-%Y %H:%M")
            meta = h["meta"]
            st.markdown(
                f"**{t}** — {meta['nama']} | {meta['jenis']} | {meta['jumlah']} project | {meta['level']}"
            )
            st.text(h["text"])
            st.divider()
