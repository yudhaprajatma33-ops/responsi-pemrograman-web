import os

class Config:
    """Konfigurasi aplikasi Flask"""
    
    # Konfigurasi Database MySQL (Membaca Environment Variables Vercel)
    HOST = os.environ.get("DB_HOST", "dbkampus-students2212.d.aivencloud.com")
    PORT = int(os.environ.get("DB_PORT", 26243))
    USER = os.environ.get("DB_USER", "avnadmin")
    PASSWORD = os.environ.get("DB_PASSWORD", "AVNS_i3pU5bPDeWCHjlcSGo-")
    DATABASE = os.environ.get("DB_NAME", "defaultdb")
    
    # Secret Key Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "praktikum-flask-2026")
    
    # Konfigurasi Flask
    DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
