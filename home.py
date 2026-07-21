from flask import Blueprint
from flask import render_template
from flask import flash

from database import get_connection

# ==========================================
# Blueprint Home
# URL : /
# ==========================================

home_bp = Blueprint(
    "home",
    __name__
)


# ==========================================
# Dashboard
# ==========================================
@home_bp.route("/")
def index():

    conn = get_connection()

    if conn is None:

        flash(
            "Koneksi database gagal.",
            "danger"
        )

        return render_template(
            "index.html",
            total_prodi=0,
            total_mahasiswa=0,
            total_matakuliah=0,
            total_krs=0,
            statistik=[],
            terbaru=[]
        )

    cursor = conn.cursor(dictionary=True)

    # =====================================
    # Jumlah Program Studi
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM program_studi
    """)

    total_prodi = cursor.fetchone()["total"]

    # =====================================
    # Jumlah Mahasiswa
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM mahasiswa
    """)

    total_mahasiswa = cursor.fetchone()["total"]

    # =====================================
    # Jumlah Mata Kuliah
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM mata_kuliah
    """)

    total_matakuliah = cursor.fetchone()["total"]

    # =====================================
    # Jumlah KRS
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM krs
    """)

    total_krs = cursor.fetchone()["total"]

    # =====================================
    # Statistik Mahasiswa per Program Studi
    # =====================================

    cursor.execute("""
        SELECT

            p.nama_prodi,

            COALESCE(COUNT(m.nim),0) AS jumlah

        FROM program_studi p

        LEFT JOIN mahasiswa m

            ON p.id = m.prodi_id

        GROUP BY

            p.id,
            p.nama_prodi

        ORDER BY

            p.nama_prodi
    """)

    statistik = cursor.fetchall()

    # =====================================
    # Lima KRS Terbaru
    # =====================================

    cursor.execute("""
        SELECT

            k.id,

            m.nim,

            m.nama,

            p.nama_prodi,

            mk.kode,

            mk.nama_mk,

            mk.sks

        FROM krs k

        INNER JOIN mahasiswa m

            ON k.nim = m.nim

        INNER JOIN program_studi p

            ON m.prodi_id = p.id

        INNER JOIN mata_kuliah mk

            ON k.kode = mk.kode

        ORDER BY

            k.id DESC

        LIMIT 5
    """)

    terbaru = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(

        "index.html",

        total_prodi=total_prodi,

        total_mahasiswa=total_mahasiswa,

        total_matakuliah=total_matakuliah,

        total_krs=total_krs,

        statistik=statistik,

        terbaru=terbaru
    )