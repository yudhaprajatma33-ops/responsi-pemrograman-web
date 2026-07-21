from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from database import get_connection


# ==========================================
# Blueprint Mahasiswa
# URL Prefix : /mahasiswa
# ==========================================

mahasiswa_bp = Blueprint(
    "mahasiswa",
    __name__,
    url_prefix="/mahasiswa"
)


# ==========================================
# Menampilkan Data Mahasiswa
# ==========================================
@mahasiswa_bp.route("/")
def mahasiswa():

    conn = get_connection()

    if conn is None:
        flash("Koneksi database gagal.", "danger")
        return redirect(url_for("home.index"))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT

            m.nim,
            m.nama,
            m.email,
            m.prodi_id,

            p.nama_prodi

        FROM mahasiswa m

        INNER JOIN program_studi p

            ON m.prodi_id = p.id

        ORDER BY
            m.nama ASC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "mahasiswa/list.html",
        mahasiswa=data
    )


# ==========================================
# Form Tambah
# ==========================================
@mahasiswa_bp.route("/tambah")
def tambah_mahasiswa():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nama_prodi
        FROM program_studi
        ORDER BY nama_prodi
    """)

    prodi = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "mahasiswa/tambah.html",
        prodi=prodi
    )


# ==========================================
# Simpan Data
# ==========================================
@mahasiswa_bp.route("/simpan", methods=["POST"])
def simpan_mahasiswa():

    nim = request.form["nim"].strip()
    nama = request.form["nama"].strip()
    email = request.form["email"].strip()
    prodi_id = request.form["prodi_id"]

    if nim == "" or nama == "" or prodi_id == "":

        flash(
            "Data wajib diisi.",
            "warning"
        )

        return redirect(
            url_for("mahasiswa.tambah_mahasiswa")
        )

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    # cek NIM

    cursor.execute("""
        SELECT nim
        FROM mahasiswa
        WHERE nim=%s
    """, (nim,))

    if cursor.fetchone():

        cursor.close()
        conn.close()

        flash(
            "NIM sudah digunakan.",
            "warning"
        )

        return redirect(
            url_for("mahasiswa.tambah_mahasiswa")
        )

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO mahasiswa

        (
            nim,
            nama,
            email,
            prodi_id
        )

        VALUES

        (%s,%s,%s,%s)

    """, (
        nim,
        nama,
        email,
        prodi_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Data mahasiswa berhasil ditambahkan.",
        "success"
    )

    return redirect(
        url_for("mahasiswa.mahasiswa")
    )


# ==========================================
# Form Edit
# ==========================================
@mahasiswa_bp.route("/edit/<nim>")
def edit_mahasiswa(nim):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM mahasiswa
        WHERE nim=%s
    """, (nim,))

    mahasiswa = cursor.fetchone()

    if mahasiswa is None:

        cursor.close()
        conn.close()

        flash(
            "Data tidak ditemukan.",
            "danger"
        )

        return redirect(
            url_for("mahasiswa.mahasiswa")
        )

    cursor.execute("""
        SELECT
            id,
            nama_prodi
        FROM program_studi
        ORDER BY nama_prodi
    """)

    prodi = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "mahasiswa/edit.html",
        mahasiswa=mahasiswa,
        prodi=prodi
    )


# ==========================================
# Update Data
# ==========================================
@mahasiswa_bp.route("/update/<nim>", methods=["POST"])
def update_mahasiswa(nim):

    nama = request.form["nama"].strip()
    email = request.form["email"].strip()
    prodi_id = request.form["prodi_id"]

    if nama == "" or prodi_id == "":

        flash(
            "Data wajib diisi.",
            "warning"
        )

        return redirect(
            url_for(
                "mahasiswa.edit_mahasiswa",
                nim=nim
            )
        )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE mahasiswa

        SET

            nama=%s,
            email=%s,
            prodi_id=%s

        WHERE

            nim=%s
    """, (
        nama,
        email,
        prodi_id,
        nim
    ))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Data mahasiswa berhasil diperbarui.",
        "success"
    )

    return redirect(
        url_for("mahasiswa.mahasiswa")
    )


# ==========================================
# Hapus Data
# ==========================================
@mahasiswa_bp.route("/hapus/<nim>")
def hapus_mahasiswa(nim):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    # cek apakah mahasiswa memiliki KRS

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM krs
        WHERE nim=%s
    """, (nim,))

    hasil = cursor.fetchone()

    if hasil["total"] > 0:

        cursor.close()
        conn.close()

        flash(
            "Mahasiswa tidak dapat dihapus karena masih memiliki data KRS.",
            "danger"
        )

        return redirect(
            url_for("mahasiswa.mahasiswa")
        )

    cursor = conn.cursor()

    cursor.execute("""
        DELETE
        FROM mahasiswa
        WHERE nim=%s
    """, (nim,))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Data mahasiswa berhasil dihapus.",
        "success"
    )

    return redirect(
        url_for("mahasiswa.mahasiswa")
    )