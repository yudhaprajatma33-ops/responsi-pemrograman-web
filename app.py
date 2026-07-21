from flask import Flask

from config import Config

from routes.home import home_bp
from routes.prodi import prodi_bp
from routes.mahasiswa import mahasiswa_bp
from routes.matakuliah import matakuliah_bp
from routes.krs import krs_bp


def create_app():
    """
    Membuat dan mengkonfigurasi aplikasi Flask.
    """

    app = Flask(__name__)

    # Memuat konfigurasi aplikasi
    app.config.from_object(Config)

    # Mendaftarkan Blueprint
    app.register_blueprint(home_bp)
    app.register_blueprint(prodi_bp)
    app.register_blueprint(mahasiswa_bp)
    app.register_blueprint(matakuliah_bp)
    app.register_blueprint(krs_bp)

    return app


app = create_app()
