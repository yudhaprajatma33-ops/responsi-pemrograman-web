from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from database import get_connection


# ==========================================
# Blueprint KRS
# URL Prefix : /krs
# ==========================================

krs_bp = Blueprint(
    "krs",
    __name__,
    url_prefix="/krs"
)


# ==========================================
# Menampilkan Data KRS
# ==========================================
@krs_bp.route("/")
def krs():

    conn = get_connection()

    if conn is None:
        flash("Koneksi database gagal.", "danger")
        return redirect(url_for("home.index"))

    cursor = conn.cursor(dictionary=True)

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
            m.nama,
            mk.kode
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "krs/list.html",
        krs=data
    )


# ==========================================
# Form Tambah
# ==========================================
@krs_bp.route("/tambah")
def tambah_krs():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            nim,
            nama
        FROM mahasiswa
        ORDER BY nama
    """)

    mahasiswa = cursor.fetchall()

    cursor.execute("""
        SELECT
            kode,
            nama_mk,
            sks
        FROM mata_kuliah
        ORDER BY kode
    """)

    matakuliah = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "krs/tambah.html",
        mahasiswa=mahasiswa,
        matakuliah=matakuliah
    )


# ==========================================
# Simpan Data
# ==========================================
@krs_bp.route("/simpan", methods=["POST"])
def simpan_krs():

    nim = request.form["nim"]
    kode = request.form["kode"]

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    # Cek apakah mahasiswa sudah mengambil mata kuliah tersebut
    cursor.execute("""
        SELECT id
        FROM krs
        WHERE nim=%s
        AND kode=%s
    """, (nim, kode))

    if cursor.fetchone():

        cursor.close()
        conn.close()

        flash(
            "Mahasiswa sudah mengambil mata kuliah tersebut.",
            "warning"
        )

        return redirect(
            url_for("krs.tambah_krs")
        )

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO krs

        (
            nim,
            kode
        )

        VALUES

        (%s,%s)

    """, (nim, kode))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Data KRS berhasil ditambahkan.",
        "success"
    )

    return redirect(
        url_for("krs.krs")
    )


# ==========================================
# Form Edit
# ==========================================
@krs_bp.route("/edit/<int:id>")
def edit_krs(id):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM krs
        WHERE id=%s
    """, (id,))

    data = cursor.fetchone()

    if data is None:

        cursor.close()
        conn.close()

        flash(
            "Data tidak ditemukan.",
            "danger"
        )

        return redirect(
            url_for("krs.krs")
        )

    cursor.execute("""
        SELECT
            nim,
            nama
        FROM mahasiswa
        ORDER BY nama
    """)

    mahasiswa = cursor.fetchall()

    cursor.execute("""
        SELECT
            kode,
            nama_mk
        FROM mata_kuliah
        ORDER BY kode
    """)

    matakuliah = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "krs/edit.html",
        krs=data,
        mahasiswa=mahasiswa,
        matakuliah=matakuliah
    )


# ==========================================
# Update Data
# ==========================================
@krs_bp.route("/update/<int:id>", methods=["POST"])
def update_krs(id):

    nim = request.form["nim"]
    kode = request.form["kode"]

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    # Cek kombinasi NIM dan Kode selain record saat ini
    cursor.execute("""
        SELECT id
        FROM krs
        WHERE nim=%s
        AND kode=%s
        AND id<>%s
    """, (nim, kode, id))

    if cursor.fetchone():

        cursor.close()
        conn.close()

        flash(
            "Data KRS sudah ada.",
            "warning"
        )

        return redirect(
            url_for("krs.edit_krs", id=id)
        )

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE krs

        SET

            nim=%s,

            kode=%s

        WHERE

            id=%s

    """, (
        nim,
        kode,
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Data KRS berhasil diperbarui.",
        "success"
    )

    return redirect(
        url_for("krs.krs")
    )


# ==========================================
# Hapus Data
# ==========================================
@krs_bp.route("/hapus/<int:id>")
def hapus_krs(id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE
        FROM krs
        WHERE id=%s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Data KRS berhasil dihapus.",
        "success"
    )

    return redirect(
        url_for("krs.krs")
    )