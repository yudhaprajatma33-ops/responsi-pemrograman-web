import pymysql
import pymysql.cursors
from config import Config

class SafeConnection:
    """
    Wrapper agar PyMySQL bisa menerima panggilan cursor(dictionary=True) 
    tanpa menyebabkan TypeError.
    """
    def __init__(self, raw_conn):
        self.raw_conn = raw_conn

    def cursor(self, dictionary=False):
        # Selalu kembalikan DictCursor apapun nilai dictionary-nya
        return self.raw_conn.cursor(pymysql.cursors.DictCursor)

    def commit(self):
        return self.raw_conn.commit()

    def rollback(self):
        return self.raw_conn.rollback()

    def close(self):
        return self.raw_conn.close()

def get_connection():
    """
    Membuat koneksi ke database MySQL Aiven.
    """
    try:
        connection = pymysql.connect(
            host=Config.HOST,
            port=int(Config.PORT),
            user=Config.USER,
            password=Config.PASSWORD,
            database=Config.DATABASE,
            autocommit=True
        )
        return SafeConnection(connection)
    except Exception as e:
        print(f"Gagal terhubung ke database: {e}")
        return None