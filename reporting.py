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
    "<div class='sub-title'>Laporan 1 paragraf + catatan evaluasi (jumlah project, style bahasa, 5 variasi)</div>",
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
        "The student can proceed to the next stage with confidence.",
        "Excellent progress—ready for the next project."
    ],
    "Cukup": [
        "Further practice is recommended to improve focus and consistency.",
        "Additional exercises are suggested to strengthen understanding."
    ],
    "Perlu Bimbingan": [
        "More intensive guidance is recommended in the next session.",
        "Concept reinforcement and step-by-step support are needed."
    ]
}

# =========================================================
# UTIL JUMLAH PROJECT
# =========================================================
def project_count_text(jumlah, bahasa):
    if bahasa == "Indonesia":
        return "satu project" if jumlah == 1 else f"{jumlah} project"
    return "one project" if jumlah == 1 else f"{jumlah} projects"

# =========================================================
# CORE: GENERATE REPORT (STYLE: Formal/Santai/Motivasional)
# =========================================================
def generate_project_report(nama, jenis, status, level, progres, bahasa, jumlah_project, style):
    n = nama.strip().title()
    j_raw = jenis.lower()
    j_id = "coding" if j_raw == "coding" else "robotic"
    j_en = "coding" if j_raw == "coding" else "robotics"

    c = project_count_text(jumlah_project, bahasa)

    if bahasa == "Indonesia":
        p = "melanjutkan project sebelumnya" if progres == "Melanjutkan Project" else "mengerjakan project baru"
        hasil = random.choice([
            "project dinyatakan selesai dan dapat diuji dengan baik" if status == "Selesai" else "project belum selesai karena masih ada bagian yang perlu diperbaiki",
            "pengerjaan berjalan sesuai target" if status == "Selesai" else "pengerjaan belum tuntas dan masih memerlukan evaluasi lanjutan",
            "hasilnya berjalan sesuai yang diharapkan" if status == "Selesai" else "hasilnya belum dapat dijalankan sepenuhnya karena masih terdapat kesalahan",
        ])

        templates = {
            "Formal": {
                "Baik": [
                    "{n} {p} dengan mengerjakan {c} pada bidang {j} dengan kinerja yang sangat baik, menunjukkan kemandirian, konsistensi fokus, serta pemahaman konsep yang kuat sehingga {hasil}.",
                    "Dalam sesi pembelajaran ini, {n} {p} dan mengerjakan {c} pada project {j} secara terstruktur dan mandiri, dengan kualitas kerja yang sangat baik sehingga {hasil}.",
                    "{n} menunjukkan performa yang unggul saat {p} dengan mengerjakan {c} pada project {j}, mampu mengikuti instruksi dengan tepat serta menjaga ketelitian hingga {hasil}.",
                    "{n} {p} dengan mengerjakan {c} pada project {j} dengan hasil yang sangat memuaskan, memperlihatkan fokus yang stabil, kerapian kerja, dan pemahaman konsep yang matang sehingga {hasil}.",
                    "Selama kegiatan berlangsung, {n} {p} dan mengerjakan {c} pada project {j} dengan kemampuan yang sangat baik, ditunjukkan oleh kemandirian dan penerapan konsep yang tepat hingga {hasil}."
                ],
                "Cukup": [
                    "{n} {p} dengan mengerjakan {c} pada project {j} dengan capaian yang cukup baik, meskipun masih memerlukan penguatan fokus dan ketelitian hingga {hasil}.",
                    "Pada kegiatan ini, {n} {p} dan mengerjakan {c} pada project {j} dengan hasil yang cukup memadai, namun masih membutuhkan arahan ringan agar pengerjaan lebih konsisten sehingga {hasil}.",
                    "{n} menunjukkan progres yang cukup baik saat {p} dengan mengerjakan {c} pada project {j}, meskipun konsistensi fokus perlu ditingkatkan hingga {hasil}.",
                    "Dalam sesi ini, {n} {p} dan mengerjakan {c} pada project {j} dengan pemahaman dasar yang cukup baik, namun masih diperlukan latihan lanjutan untuk meningkatkan kerapian hingga {hasil}.",
                    "{n} {p} dengan mengerjakan {c} pada project {j} dengan hasil yang cukup baik, walaupun masih dibutuhkan pendampingan ringan pada beberapa bagian sampai {hasil}."
                ],
                "Perlu Bimbingan": [
                    "{n} {p} dengan mengerjakan {c} pada project {j}, namun masih menghadapi kendala dalam fokus dan pemahaman konsep sehingga {hasil} dan diperlukan pendampingan lanjutan.",
                    "Dalam sesi ini, {n} {p} dan mengerjakan {c} pada project {j} dengan hasil yang belum optimal, sehingga {hasil} dan perlu bimbingan lebih intensif.",
                    "{n} {p} dengan mengerjakan {c} pada project {j}, tetapi konsistensi kerja belum stabil sehingga {hasil} dan diperlukan penguatan konsep dasar.",
                    "Selama proses berlangsung, {n} {p} dan mengerjakan {c} pada project {j}, namun beberapa langkah masih sering terlewat sehingga {hasil} dan perlu pendampingan bertahap.",
                    "{n} {p} dengan mengerjakan {c} pada project {j} dengan tantangan yang cukup banyak, sehingga {hasil} dan perlu dukungan lebih dekat untuk menjaga alur kerja."
                ],
            },

            "Santai": {
                "Baik": [
                    "{n} {p} sambil mengerjakan {c} di project {j}, kerjanya rapi, fokusnya stabil, dan hasilnya mantap karena {hasil}.",
                    "Di sesi ini, {n} {p} dan mengerjakan {c} di project {j} dengan sangat lancar, kelihatan mandiri dan paham konsep sampai {hasil}.",
                    "{n} {p} sambil mengerjakan {c} di project {j} dengan performa keren, fokusnya terjaga dan eksekusinya bagus sehingga {hasil}.",
                    "Saat belajar hari ini, {n} {p} dan menyelesaikan {c} di project {j} dengan nyaman, langkahnya runtut dan hasilnya oke banget karena {hasil}.",
                    "{n} terlihat percaya diri saat {p} dan mengerjakan {c} di project {j}, kerja cepat tapi tetap rapi sampai akhirnya {hasil}."
                ],
                "Cukup": [
                    "{n} {p} dan mengerjakan {c} di project {j} dengan hasil yang cukup oke, meski kadang masih perlu diingatkan supaya fokus sampai {hasil}.",
                    "Di sesi ini, {n} {p} sambil mengerjakan {c} di project {j}, hasilnya lumayan tapi konsistensinya masih perlu latihan karena {hasil}.",
                    "{n} {p} dan mengerjakan {c} di project {j} dengan pemahaman yang cukup, walau masih perlu arahan ringan biar lebih rapi sampai {hasil}.",
                    "Saat {p}, {n} mengerjakan {c} di project {j} dengan progres cukup baik, tapi fokusnya masih naik turun sampai {hasil}.",
                    "{n} {p} sambil mengerjakan {c} di project {j} dengan hasil cukup, tinggal ditingkatkan lagi ketelitian dan ritmenya sampai {hasil}."
                ],
                "Perlu Bimbingan": [
                    "{n} {p} dan mengerjakan {c} di project {j}, tapi fokusnya masih sering teralihkan sehingga {hasil} dan masih perlu pendampingan.",
                    "Di sesi ini, {n} {p} sambil mengerjakan {c} di project {j}, namun masih bingung di beberapa langkah jadi {hasil} dan butuh bimbingan lebih dekat.",
                    "{n} {p} dan mengerjakan {c} di project {j}, prosesnya masih belum stabil sehingga {hasil} dan perlu latihan bertahap.",
                    "Saat {p}, {n} mengerjakan {c} di project {j} tapi masih butuh arahan sering agar langkahnya tidak terlewat, jadi {hasil}.",
                    "{n} {p} sambil mengerjakan {c} di project {j}, tapi masih kesulitan jaga alur kerja sehingga {hasil} dan perlu penguatan konsep."
                ],
            },

            "Motivasional": {
                "Baik": [
                    "{n} {p} dengan mengerjakan {c} pada project {j} dengan sangat baik, menunjukkan semangat belajar yang tinggi, fokus yang konsisten, serta kemandirian yang kuat sehingga {hasil}, sebuah pencapaian yang patut diapresiasi.",
                    "Dalam sesi ini, {n} {p} dan menyelesaikan {c} pada project {j} dengan penuh keyakinan, membuktikan bahwa fokus dan kerja keras mampu menghasilkan {hasil}.",
                    "{n} menunjukkan progres yang luar biasa saat {p} dengan mengerjakan {c} pada project {j}, mampu menerapkan konsep dengan baik hingga {hasil}, dan ini menjadi langkah besar untuk naik ke level berikutnya.",
                    "Selama kegiatan berlangsung, {n} {p} dan mengerjakan {c} pada project {j} dengan performa kuat, menjaga ketelitian dan konsistensi hingga {hasil}, yang menandakan kesiapan untuk tantangan berikutnya.",
                    "{n} {p} dengan mengerjakan {c} pada project {j} secara mandiri dan terstruktur, menunjukkan perkembangan yang sangat positif hingga {hasil}, dan ini adalah bukti kemampuan {n} terus bertumbuh."
                ],
                "Cukup": [
                    "{n} {p} dengan mengerjakan {c} pada project {j} dengan hasil yang cukup baik, dan dengan latihan yang konsisten {n} berpotensi mencapai hasil yang lebih optimal meskipun saat ini {hasil}.",
                    "Dalam sesi ini, {n} {p} dan mengerjakan {c} pada project {j} dengan progres yang cukup baik, walaupun masih perlu penguatan fokus hingga {hasil}, namun langkah ini sudah menunjukkan perkembangan.",
                    "{n} menunjukkan kemauan belajar yang positif saat {p} dengan mengerjakan {c} pada project {j}, dan meskipun {hasil}, latihan rutin akan membantu {n} menjadi lebih stabil.",
                    "Saat {p}, {n} mengerjakan {c} pada project {j} dengan pemahaman dasar yang cukup, meskipun masih perlu pendampingan ringan hingga {hasil}, ini tetap menjadi bagian penting dari proses berkembang.",
                    "{n} {p} dengan mengerjakan {c} pada project {j}, dan walau {hasil}, konsistensi akan terbentuk dengan latihan tambahan dan evaluasi langkah kerja."
                ],
                "Perlu Bimbingan": [
                    "{n} {p} dengan mengerjakan {c} pada project {j}, dan meskipun masih ada kendala fokus serta pemahaman, {n} tetap memiliki potensi besar untuk berkembang walaupun saat ini {hasil}.",
                    "Dalam sesi ini, {n} {p} dan mengerjakan {c} pada project {j}; walaupun {hasil}, setiap proses adalah langkah belajar dan {n} perlu pendampingan bertahap untuk menjadi lebih percaya diri.",
                    "{n} {p} dengan mengerjakan {c} pada project {j} dengan tantangan yang cukup banyak, sehingga {hasil}, namun dengan bimbingan yang tepat {n} dapat memperbaiki alur kerja secara perlahan.",
                    "Saat {p}, {n} mengerjakan {c} pada project {j}, meskipun {hasil}, latihan terarah dan penguatan konsep akan membantu {n} lebih fokus dan siap melanjutkan.",
                    "{n} {p} dengan mengerjakan {c} pada project {j}, walaupun {hasil}, ini menjadi dasar penting untuk membangun pemahaman dan kebiasaan kerja yang lebih stabil."
                ],
            }
        }

        template = random.choice(templates[style][level])
        return template.format(n=n, p=p, c=c, j=j_id, hasil=hasil)

    # ENGLISH
    p = "continued the previous project" if progres == "Melanjutkan Project" else "worked on a new project"
    hasil = random.choice([
        "the project was completed and ran successfully" if status == "Selesai" else "the project was not completed due to remaining issues",
        "the task was completed as expected" if status == "Selesai" else "the task remains unfinished and requires further correction",
        "the project executed well during testing" if status == "Selesai" else "the project could not run fully because some errors remain",
    ])

    templates_en = {
        "Formal": {
            "Baik": [
                "{n} {p} by completing {c} in the {j} project with excellent performance, demonstrating independence, consistent focus, and strong understanding, resulting in {hasil}.",
                "{n} {p} and completed {c} in the {j} project in a structured manner with strong accuracy, and {hasil}."
            ],
            "Cukup": [
                "{n} {p} by working on {c} in the {j} project with fairly good results, although some guidance was still needed, and {hasil}.",
                "{n} {p} and worked on {c} in the {j} project with acceptable progress, with consistency still requiring improvement, and {hasil}."
            ],
            "Perlu Bimbingan": [
                "{n} {p} by working on {c} in the {j} project but faced challenges in focus and understanding, therefore {hasil} and further guidance is recommended.",
                "{n} {p} and worked on {c} in the {j} project with unstable progress, so {hasil} and close assistance is still required."
            ]
        },
        "Santai": {
            "Baik": [
                "{n} {p} and finished {c} in the {j} project with great focus and smooth execution, so {hasil}.",
                "{n} {p} and worked on {c} in the {j} project very confidently, and {hasil}."
            ],
            "Cukup": [
                "{n} {p} and worked on {c} in the {j} project with decent results, though focus still needs practice, and {hasil}.",
                "{n} {p} and handled {c} in the {j} project fairly well, but consistency still needs improvement, and {hasil}."
            ],
            "Perlu Bimbingan": [
                "{n} {p} and worked on {c} in the {j} project but still needs close guidance to stay on track, so {hasil}.",
                "{n} {p} and worked on {c} in the {j} project with some difficulties, so {hasil} and more support is needed."
            ]
        },
        "Motivational": {
            "Baik": [
                "{n} {p} by completing {c} in the {j} project with excellent effort and strong focus, resulting in {hasil}, which is a great achievement to build on.",
                "{n} {p} and completed {c} in the {j} project with strong progress, leading to {hasil}, showing readiness for the next challenge."
            ],
            "Cukup": [
                "{n} {p} by working on {c} in the {j} project with fair progress; although {hasil}, consistent practice will lead to better stability.",
                "{n} {p} and worked on {c} in the {j} project with decent effort; even though {hasil}, improvement will come with regular training."
            ],
            "Perlu Bimbingan": [
                "{n} {p} by working on {c} in the {j} project; although {hasil}, this is part of the learning process and additional guidance will help progress.",
                "{n} {p} and worked on {c} in the {j} project with challenges; even though {hasil}, structured support can improve confidence and focus."
            ]
        }
    }

    template = random.choice(templates_en[style][level])
    return template.format(n=n, p=p, c=c, j=j_en, hasil=hasil)

# =========================================================
# INPUT FORM
# =========================================================
st.subheader("📝 Input Laporan Proyek")
st.markdown("<div class='small-muted'>Buat 1 laporan atau 5 variasi (Formal/Santai/Motivasional).</div>", unsafe_allow_html=True)

nama = st.text_input("Nama Anak", placeholder="Contoh: Dista")
jenis = st.selectbox("Jenis Project", ["Coding", "Robotic"])
jumlah_project = st.number_input("Jumlah Project yang Dikerjakan", min_value=1, max_value=10, value=1)
progres = st.radio("Jenis Kegiatan", ["Melanjutkan Project", "Project Baru"], horizontal=True)
status = st.radio("Status Project", ["Selesai", "Tidak Selesai"], horizontal=True)
level = st.selectbox("Level Performa", ["Baik", "Cukup", "Perlu Bimbingan"])
bahasa = st.selectbox("Bahasa Laporan", ["Indonesia", "English"])
style = st.selectbox("Gaya Bahasa Laporan", ["Formal", "Santai", "Motivasional"])

# =========================================================
# GENERATE REPORT
# =========================================================
colA, colB = st.columns(2)
with colA:
    gen = st.button("🚀 Buat Laporan", use_container_width=True)
with colB:
    regen = st.button("🔁 Buat Variasi Baru (5x)", use_container_width=True)

if gen:
    if not nama.strip():
        st.warning("Nama anak wajib diisi.")
    else:
        laporan = generate_project_report(
            nama, jenis, status, level, progres, bahasa, jumlah_project, style
        )
        meta = {
            "nama": nama.strip().title(),
            "jenis": jenis,
            "jumlah": jumlah_project,
            "progres": progres,
            "status": status,
            "level": level,
            "bahasa": bahasa,
            "style": style
        }
        save_history(laporan, meta)

        st.subheader("📄 Hasil Laporan AI")
        st.text_area("", laporan, height=160)

        # NOTE
        if bahasa == "Indonesia":
            st.info(f"📝 **Catatan:** {random.choice(NOTE_ID[level])}")
        else:
            st.info(f"📝 **Note:** {random.choice(NOTE_EN[level])}")

if regen:
    if not nama.strip():
        st.warning("Nama anak wajib diisi.")
    else:
        st.subheader("🔁 5 Variasi Laporan (Berbeda)")
        used = set()
        variations = 0

        while variations < 5:
            laporan = generate_project_report(
                nama, jenis, status, level, progres, bahasa, jumlah_project, style
            )
            if laporan in used:
                continue
            used.add(laporan)
            variations += 1

            meta = {
                "nama": nama.strip().title(),
                "jenis": jenis,
                "jumlah": jumlah_project,
                "progres": progres,
                "status": status,
                "level": level,
                "bahasa": bahasa,
                "style": style,
                "variasi": variations
            }
            save_history(laporan, meta)

            st.text_area(f"Variasi {variations}", laporan, height=120)

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
            meta_line = (
                f"{meta.get('nama','-')} | {meta.get('jenis','-')} | {meta.get('jumlah','-')} project | "
                f"{meta.get('progres','-')} | {meta.get('status','-')} | {meta.get('level','-')} | "
                f"{meta.get('bahasa','-')} | {meta.get('style','-')}"
            )
            if "variasi" in meta:
                meta_line += f" | Variasi {meta['variasi']}"
            st.markdown(f"**{t}** — {meta_line}")
            st.text(h["text"])
            st.divider()
