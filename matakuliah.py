from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from database import get_connection


# ==========================================
# Blueprint Mata Kuliah
# URL Prefix : /matakuliah
# ==========================================

matakuliah_bp = Blueprint(
    "matakuliah",
    __name__,
    url_prefix="/matakuliah"
)


# ==========================================
# Menampilkan Data Mata Kuliah
# ==========================================
@matakuliah_bp.route("/")
def matakuliah():

    conn = get_connection()

    if conn is None:
        flash("Koneksi database gagal.", "danger")
        return redirect(url_for("home.index"))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            kode,
            nama_mk,
            sks
        FROM mata_kuliah
        ORDER BY kode ASC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "matakuliah/list.html",
        matakuliah=data
    )


# ==========================================
# Form Tambah
# ==========================================
@matakuliah_bp.route("/tambah")
def tambah_matakuliah():

    return render_template(
        "matakuliah/tambah.html"
    )


# ==========================================
# Simpan Data
# ==========================================
@matakuliah_bp.route("/simpan", methods=["POST"])
def simpan_matakuliah():

    kode = request.form["kode"].strip().upper()
    nama_mk = request.form["nama_mk"].strip()
    sks = request.form["sks"]

    if kode == "" or nama_mk == "" or sks == "":
        flash("Semua field wajib diisi.", "warning")
        return redirect(url_for("matakuliah.tambah_matakuliah"))

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    # Cek kode mata kuliah
    cursor.execute("""
        SELECT kode
        FROM mata_kuliah
        WHERE kode=%s
    """, (kode,))

    if cursor.fetchone():

        cursor.close()
        conn.close()

        flash("Kode Mata Kuliah sudah digunakan.", "warning")

        return redirect(
            url_for("matakuliah.tambah_matakuliah")
        )

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mata_kuliah
        (
            kode,
            nama_mk,
            sks
        )
        VALUES
        (%s,%s,%s)
    """, (kode, nama_mk, sks))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Data Mata Kuliah berhasil ditambahkan.",
        "success"
    )

    return redirect(
        url_for("matakuliah.matakuliah")
    )


# ==========================================
# Form Edit
# ==========================================
@matakuliah_bp.route("/edit/<kode>")
def edit_matakuliah(kode):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM mata_kuliah
        WHERE kode=%s
    """, (kode,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if data is None:

        flash(
            "Data tidak ditemukan.",
            "danger"
        )

        return redirect(
            url_for("matakuliah.matakuliah")
        )

    return render_template(
        "matakuliah/edit.html",
        mk=data
    )


# ==========================================
# Update Data
# ==========================================
@matakuliah_bp.route("/update/<kode>", methods=["POST"])
def update_matakuliah(kode):

    nama_mk = request.form["nama_mk"].strip()
    sks = request.form["sks"]

    if nama_mk == "" or sks == "":

        flash(
            "Semua field wajib diisi.",
            "warning"
        )

        return redirect(
            url_for(
                "matakuliah.edit_matakuliah",
                kode=kode
            )
        )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE mata_kuliah

        SET

            nama_mk=%s,

            sks=%s

        WHERE

            kode=%s
    """, (nama_mk, sks, kode))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Data Mata Kuliah berhasil diperbarui.",
        "success"
    )

    return redirect(
        url_for("matakuliah.matakuliah")
    )


# ==========================================
# Hapus Data
# ==========================================
@matakuliah_bp.route("/hapus/<kode>")
def hapus_matakuliah(kode):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    # Cek apakah mata kuliah digunakan pada KRS
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM krs
        WHERE kode=%s
    """, (kode,))

    hasil = cursor.fetchone()

    if hasil["total"] > 0:

        cursor.close()
        conn.close()

        flash(
            "Mata Kuliah tidak dapat dihapus karena sudah digunakan pada data KRS.",
            "danger"
        )

        return redirect(
            url_for("matakuliah.matakuliah")
        )

    cursor = conn.cursor()

    cursor.execute("""
        DELETE
        FROM mata_kuliah
        WHERE kode=%s
    """, (kode,))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Data Mata Kuliah berhasil dihapus.",
        "success"
    )

    return redirect(
        url_for("matakuliah.matakuliah")
    )