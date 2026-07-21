from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from database import get_connection

# =====================================================
# Blueprint Program Studi
# URL Prefix : /prodi
# =====================================================

prodi_bp = Blueprint(
    "prodi",
    __name__,
    url_prefix="/prodi"
)


# =====================================================
# Menampilkan seluruh data Program Studi
# =====================================================
@prodi_bp.route("/")
def prodi():

    conn = get_connection()

    if conn is None:
        flash("Koneksi database gagal.", "danger")
        return redirect(url_for("home.index"))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nama_prodi
        FROM program_studi
        ORDER BY nama_prodi ASC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "prodi/list.html",
        prodi=data
    )


# =====================================================
# Form Tambah Program Studi
# =====================================================
@prodi_bp.route("/tambah")
def tambah_prodi():

    return render_template(
        "prodi/tambah.html"
    )


# =====================================================
# Simpan Data
# =====================================================
@prodi_bp.route("/simpan", methods=["POST"])
def simpan_prodi():

    nama_prodi = request.form["nama_prodi"].strip()

    if nama_prodi == "":
        flash("Nama Program Studi tidak boleh kosong.", "warning")
        return redirect(url_for("prodi.tambah_prodi"))

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    # Cek apakah sudah ada
    cursor.execute("""
        SELECT id
        FROM program_studi
        WHERE nama_prodi=%s
    """, (nama_prodi,))

    cek = cursor.fetchone()

    if cek:

        flash("Program Studi sudah ada.", "warning")

        cursor.close()
        conn.close()

        return redirect(url_for("prodi.tambah_prodi"))

    # Simpan data
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO program_studi
        (nama_prodi)
        VALUES
        (%s)
    """, (nama_prodi,))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Program Studi berhasil ditambahkan.", "success")

    return redirect(
        url_for("prodi.prodi")
    )


# =====================================================
# Form Edit
# =====================================================
@prodi_bp.route("/edit/<int:id>")
def edit_prodi(id):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            *
        FROM program_studi
        WHERE id=%s
    """, (id,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if data is None:

        flash("Data tidak ditemukan.", "danger")

        return redirect(
            url_for("prodi.prodi")
        )

    return render_template(
        "prodi/edit.html",
        prodi=data
    )


# =====================================================
# Update Data
# =====================================================
@prodi_bp.route("/update/<int:id>", methods=["POST"])
def update_prodi(id):

    nama_prodi = request.form["nama_prodi"].strip()

    if nama_prodi == "":

        flash(
            "Nama Program Studi tidak boleh kosong.",
            "warning"
        )

        return redirect(
            url_for(
                "prodi.edit_prodi",
                id=id
            )
        )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE program_studi

        SET
            nama_prodi=%s

        WHERE
            id=%s
    """, (nama_prodi, id))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Program Studi berhasil diperbarui.",
        "success"
    )

    return redirect(
        url_for("prodi.prodi")
    )


# =====================================================
# Hapus Data
# =====================================================
@prodi_bp.route("/hapus/<int:id>")
def hapus_prodi(id):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    # Cek apakah Program Studi masih digunakan
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM mahasiswa
        WHERE prodi_id=%s
    """, (id,))

    hasil = cursor.fetchone()

    if hasil["total"] > 0:

        cursor.close()
        conn.close()

        flash(
            "Program Studi tidak dapat dihapus karena masih digunakan oleh data Mahasiswa.",
            "danger"
        )

        return redirect(
            url_for("prodi.prodi")
        )

    cursor = conn.cursor()

    cursor.execute("""
        DELETE
        FROM program_studi
        WHERE id=%s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Program Studi berhasil dihapus.",
        "success"
    )

    return redirect(
        url_for("prodi.prodi")
    )