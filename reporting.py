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
st.markdown("<div class='sub-title'>Generator laporan perkembangan proyek anak (Rule-Based + Variasi Dinamis)</div>", unsafe_allow_html=True)

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
# VARIASI TEMPLATE (INDONESIA)
# =========================================================
ID_PEMBUKA = [
    "Pada sesi kali ini, {n} {p} pada project {j}.",
    "Dalam kegiatan pembelajaran hari ini, {n} {p} pada project {j}.",
    "Pada pertemuan terbaru, {n} {p} pada project {j}.",
    "Selama proses pembelajaran berlangsung, {n} {p} pada project {j}.",
]

ID_KONTEKS_PROGRES = {
    "Melanjutkan Project": [
        "Project ini merupakan kelanjutan dari pertemuan sebelumnya, sehingga anak perlu mengingat kembali alur kerja dan tujuan project.",
        "Karena ini project lanjutan, {n} perlu meninjau kembali langkah-langkah sebelumnya sebelum melanjutkan tahap berikutnya.",
        "Sebagai project lanjutan, fokus utama adalah menyempurnakan bagian yang belum stabil dan memastikan hasil sesuai target."
    ],
    "Project Baru": [
        "Project ini merupakan kegiatan baru, sehingga anak perlu beradaptasi dengan konsep dan alur kerja sejak awal.",
        "Sebagai project baru, {n} belajar mengenali tujuan project, komponen yang digunakan, serta tahapan pengerjaannya.",
        "Pada project baru ini, {n} diarahkan untuk memahami konsep dasar sebelum masuk ke tahap implementasi."
    ]
}

ID_JENIS_SPESIFIK = {
    "coding": [
        "Pada aspek pemrograman, {n} berlatih memahami logika, urutan eksekusi, dan ketelitian dalam menyusun instruksi.",
        "Dalam aktivitas coding, kemampuan berpikir terstruktur dan pemahaman alur program menjadi bagian penting dari proses.",
        "Kegiatan coding melatih {n} dalam menyusun langkah-langkah logis, menguji hasil, dan memperbaiki kesalahan (debugging)."
    ],
    "robotic": [
        "Pada aspek robotika, {n} berlatih mengenali komponen, menyusun rangkaian sederhana, dan memahami respon sensor/aktuator.",
        "Dalam aktivitas robotika, {n} belajar menghubungkan konsep ke praktik melalui perakitan, pengujian, dan evaluasi hasil.",
        "Kegiatan robotika menuntut ketelitian pada pemasangan komponen, pemahaman input-output, dan pengujian fungsi."
    ]
}

ID_PERILAKU_BAIK = [
    "{n} menunjukkan kemandirian yang baik dan mampu mengikuti instruksi dengan sangat tepat.",
    "Fokus {n} stabil selama pengerjaan dan {n} dapat menjaga ritme kerja dengan konsisten.",
    "{n} terlihat percaya diri saat menjalankan tahapan project dan mampu menyelesaikan tugas tanpa banyak arahan.",
    "{n} aktif bertanya untuk memastikan pemahaman, lalu menerapkan arahan dengan cepat dan rapi."
]

ID_PERILAKU_CUKUP = [
    "{n} masih membutuhkan arahan ringan pada beberapa bagian, terutama untuk menjaga ketelitian.",
    "Fokus {n} kadang teralihkan, namun dapat diarahkan kembali sehingga proses pengerjaan tetap berjalan.",
    "{n} sudah berusaha mengikuti alur project, namun konsistensi pengerjaan masih perlu ditingkatkan.",
    "{n} membutuhkan penguatan pada bagian tertentu agar pengerjaan lebih rapi dan terstruktur."
]

ID_PERILAKU_BIMBINGAN = [
    "Fokus {n} belum stabil selama proses pengerjaan sehingga perlu pendampingan lebih intensif.",
    "{n} masih memerlukan bantuan untuk melanjutkan beberapa tahapan dan membutuhkan penguatan konsentrasi.",
    "Kemandirian {n} belum optimal, sehingga perlu arahan lebih sering agar langkah kerja tidak terlewat.",
    "{n} masih kesulitan menjaga alur kerja dan memerlukan penjelasan ulang pada beberapa bagian."
]

ID_PEMAHAMAN_BAIK = [
    "Pemahaman {n} terhadap konsep utama sudah sangat baik, terlihat dari cara {n} menerapkan langkah kerja secara tepat.",
    "{n} mampu menghubungkan konsep dengan praktik, dan dapat menjelaskan kembali inti dari project dengan baik.",
    "{n} memahami tujuan project dan mampu melakukan penyesuaian kecil saat diperlukan."
]

ID_PEMAHAMAN_CUKUP = [
    "{n} menunjukkan pemahaman dasar yang cukup baik, meskipun masih perlu penguatan pada detail tertentu.",
    "Konsep utama sudah dipahami, namun penerapannya belum selalu konsisten dan masih membutuhkan latihan.",
    "{n} dapat mengikuti konsep dasar dengan arahan, tetapi perlu peningkatan agar lebih mandiri."
]

ID_PEMAHAMAN_BIMBINGAN = [
    "Pemahaman konsep dasar masih perlu ditingkatkan; beberapa bagian perlu dijelaskan kembali agar lebih jelas.",
    "{n} belum sepenuhnya memahami konsep yang digunakan sehingga membutuhkan pendampingan bertahap.",
    "Masih diperlukan penguatan konsep inti agar {n} lebih percaya diri dalam mengerjakan project."
]

ID_HASIL_SELESAI = [
    "Project dapat dijalankan dengan baik dan hasilnya sesuai dengan tujuan yang ditetapkan.",
    "Hasil akhir berjalan lancar saat diuji dan menunjukkan bahwa tahapan pengerjaan dilakukan dengan benar.",
    "Project berhasil diselesaikan dan dapat dieksekusi tanpa kendala berarti."
]

ID_HASIL_TIDAK_SELESAI = [
    "Project belum selesai karena masih terdapat beberapa bagian yang perlu diperbaiki sebelum bisa diuji secara menyeluruh.",
    "Pengerjaan belum tuntas; masih ada kesalahan yang perlu ditangani agar project dapat berjalan sesuai target.",
    "Project belum dapat dijalankan sepenuhnya karena beberapa komponen/logic masih perlu pembenahan."
]

ID_PENUTUP = [
    "Secara keseluruhan, perkembangan yang ditunjukkan cukup jelas dan dapat menjadi dasar untuk langkah pembelajaran berikutnya.",
    "Catatan ini dapat digunakan sebagai evaluasi untuk meningkatkan kinerja dan konsistensi di pertemuan selanjutnya.",
    "Dengan latihan yang konsisten, potensi {n} dapat berkembang lebih optimal."
]

ID_NOTE = {
    "Baik": [
        "Bisa lanjut ke project berikutnya. Pertahankan fokus dan kemandirian yang sudah baik.",
        "Siap melanjutkan ke tahap berikutnya. Semangat terus, {n}!",
        "Dapat melanjutkan ke project selanjutnya. Kerja bagus, {n}!"
    ],
    "Cukup": [
        "Perlu latihan lanjutan agar fokus dan ketelitian meningkat.",
        "Disarankan latihan tambahan pada bagian yang masih kurang konsisten.",
        "Teruskan latihan dan evaluasi langkah kerja agar hasil makin rapi."
    ],
    "Perlu Bimbingan": [
        "Perlu pendampingan lebih intensif dan penguatan konsep pada pertemuan berikutnya.",
        "Disarankan pengulangan materi dasar dan latihan bertahap agar lebih memahami alur project.",
        "Perlu fokus pada konsentrasi dan pemahaman konsep inti sebelum lanjut ke tahap berikutnya."
    ]
}

# =========================================================
# VARIASI TEMPLATE (ENGLISH)
# =========================================================
EN_OPENING = [
    "In today’s session, {n} {p} in the {j} project.",
    "During this learning session, {n} {p} in the {j} project.",
    "In the most recent meeting, {n} {p} in the {j} project.",
    "Throughout the activity, {n} {p} in the {j} project.",
]

EN_PROGRESS_CONTEXT = {
    "Melanjutkan Project": [
        "This was a continuation of the previous project, so the student needed to recall the workflow and objectives.",
        "As a continuing project, the focus was on refining unfinished parts and improving stability.",
        "Since this project continued from the last session, reviewing earlier steps was important before moving forward."
    ],
    "Project Baru": [
        "This was a new project, so the student needed to adapt to the concept and workflow from the beginning.",
        "As a new project, the student learned the goal, components, and step-by-step process.",
        "In this new project, the student focused on understanding the fundamentals before implementation."
    ]
}

EN_TYPE_SPECIFIC = {
    "coding": [
        "In programming tasks, structured thinking, execution flow, and careful debugging were emphasized.",
        "Coding activities trained the student to plan logic, test outputs, and fix errors step by step.",
        "The coding session focused on building logical sequences and improving accuracy in implementation."
    ],
    "robotic": [
        "In robotics tasks, the student practiced assembly, testing, and understanding sensor/actuator responses.",
        "Robotics activities required careful setup, input-output reasoning, and functional testing.",
        "The robotics session emphasized component handling, system testing, and evaluating results."
    ]
}

EN_BEHAVIOR_GOOD = [
    "{n} showed strong independence and followed instructions accurately.",
    "{n} maintained consistent focus and worked steadily throughout the process.",
    "{n} confidently completed each step with minimal guidance.",
    "{n} actively asked clarifying questions and applied feedback quickly."
]

EN_BEHAVIOR_OK = [
    "{n} still needed light guidance, especially to maintain accuracy.",
    "{n} occasionally lost focus but could be redirected effectively.",
    "{n} followed the workflow but consistency still needs improvement.",
    "{n} needs additional practice to work more neatly and systematically."
]

EN_BEHAVIOR_NEED = [
    "{n}'s focus was inconsistent, so closer assistance was required.",
    "{n} needed frequent support to proceed through several steps.",
    "{n} required repeated guidance to keep the workflow on track.",
    "{n} struggled to maintain a stable working process and needed step-by-step support."
]

EN_UNDERSTANDING_GOOD = [
    "{n} demonstrated a strong understanding of the core concepts and applied them correctly.",
    "{n} connected the concept to practice and could explain the project idea clearly.",
    "{n} understood the goal and could make small adjustments when needed."
]

EN_UNDERSTANDING_OK = [
    "{n} showed a fair understanding but still needs reinforcement on certain details.",
    "The main concept was understood, but application was not always consistent.",
    "{n} can follow the basics with guidance, but needs practice to be more independent."
]

EN_UNDERSTANDING_NEED = [
    "Core understanding still needs improvement; several parts should be reviewed again.",
    "{n} has not fully grasped the concepts yet and requires gradual guidance.",
    "Additional reinforcement is needed so {n} can work more confidently."
]

EN_RESULT_DONE = [
    "The project ran well during testing and matched the intended goal.",
    "The final output worked smoothly, indicating the steps were carried out correctly.",
    "The project was completed successfully and executed without major issues."
]

EN_RESULT_NOT_DONE = [
    "The project was not completed yet because several parts still need corrections before full testing.",
    "The task remains unfinished; some issues must be fixed to reach the target output.",
    "The project could not run fully due to remaining errors that require improvement."
]

EN_CLOSING = [
    "Overall, this progress can serve as a solid reference for the next learning steps.",
    "This note can be used for evaluation to improve consistency in the next session.",
    "With consistent practice, {n}'s potential can grow significantly."
]

EN_NOTE = {
    "Baik": [
        "Ready to continue to the next project. Keep up the great work, {n}!",
        "Can move forward to the next stage. Maintain the strong focus and independence.",
        "Well done—{n} can proceed to the next project."
    ],
    "Cukup": [
        "Further practice is recommended to improve focus and accuracy.",
        "Additional exercises are suggested to strengthen consistency.",
        "Keep practicing and reviewing steps to achieve cleaner results."
    ],
    "Perlu Bimbingan": [
        "More intensive guidance and concept reinforcement are recommended in the next session.",
        "It is suggested to review fundamentals and practice step-by-step before moving on.",
        "Focus on improving concentration and core understanding before advancing."
    ]
}

# =========================================================
# UTIL: PILIH KALIMAT SESUAI LEVEL
# =========================================================
def _pick_by_level(level: str, good_list, ok_list, need_list):
    if level == "Baik":
        return random.choice(good_list)
    if level == "Cukup":
        return random.choice(ok_list)
    return random.choice(need_list)

def _progress_text(progres: str, bahasa: str) -> str:
    if bahasa == "Indonesia":
        return "melanjutkan project sebelumnya" if progres == "Melanjutkan Project" else "mengerjakan project baru"
    return "continued the previous project" if progres == "Melanjutkan Project" else "worked on a new project"

def _type_text(jenis: str, bahasa: str) -> str:
    j = jenis.lower()
    if bahasa == "Indonesia":
        return "coding" if j == "coding" else "robotic"
    return "coding" if j == "coding" else "robotics"

# =========================================================
# CORE: GENERATE REPORT
# =========================================================
def generate_project_report(nama: str, jenis: str, status: str, level: str, progres: str, bahasa: str) -> str:
    n = nama.strip().title()
    j_key = jenis.lower()
    p_text = _progress_text(progres, bahasa)
    j_text = _type_text(jenis, bahasa)

    if bahasa == "Indonesia":
        opening = random.choice(ID_PEMBUKA).format(n=n, p=p_text, j=j_text)
        progress_ctx = random.choice(ID_KONTEKS_PROGRES[progres]).format(n=n)
        type_specific = random.choice(ID_JENIS_SPESIFIK[j_key]).format(n=n)
        behavior = _pick_by_level(level, ID_PERILAKU_BAIK, ID_PERILAKU_CUKUP, ID_PERILAKU_BIMBINGAN).format(n=n)
        understanding = _pick_by_level(level, ID_PEMAHAMAN_BAIK, ID_PEMAHAMAN_CUKUP, ID_PEMAHAMAN_BIMBINGAN).format(n=n)

        if status == "Selesai":
            result = random.choice(ID_HASIL_SELESAI)
        else:
            result = random.choice(ID_HASIL_TIDAK_SELESAI)

        closing = random.choice(ID_PENUTUP).format(n=n)
        note = random.choice(ID_NOTE[level]).format(n=n)

        return f"""{n}

{opening}
{progress_ctx}
{type_specific}

{behavior}
{understanding}
{result}

Note: {note}
{closing}""".strip()

    # ENGLISH
    opening = random.choice(EN_OPENING).format(n=n, p=p_text, j=j_text)
    progress_ctx = random.choice(EN_PROGRESS_CONTEXT[progres]).format(n=n)
    type_specific = random.choice(EN_TYPE_SPECIFIC[j_key]).format(n=n)
    behavior = _pick_by_level(level, EN_BEHAVIOR_GOOD, EN_BEHAVIOR_OK, EN_BEHAVIOR_NEED).format(n=n)
    understanding = _pick_by_level(level, EN_UNDERSTANDING_GOOD, EN_UNDERSTANDING_OK, EN_UNDERSTANDING_NEED).format(n=n)

    if status == "Selesai":
        result = random.choice(EN_RESULT_DONE)
    else:
        result = random.choice(EN_RESULT_NOT_DONE)

    closing = random.choice(EN_CLOSING).format(n=n)
    note = random.choice(EN_NOTE[level]).format(n=n)

    return f"""{n}

{opening}
{progress_ctx}
{type_specific}

{behavior}
{understanding}
{result}

Note: {note}
{closing}""".strip()

# =========================================================
# INPUT FORM
# =========================================================
st.subheader("📝 Input Laporan Proyek")
st.markdown("<div class='small-muted'>Isi data berikut untuk menghasilkan laporan yang panjang, rapi, dan bervariasi.</div>", unsafe_allow_html=True)

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
        meta = {"nama": nama.strip().title(), "jenis": jenis, "progres": progres, "status": status, "level": level, "bahasa": bahasa}
        save_history(laporan, meta)

        st.subheader("📄 Hasil Laporan AI")
        st.text_area("", laporan, height=360)

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
