import os
import json
import mysql.connector

class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "Access.json")
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        self.conn = mysql.connector.connect(**config)


    def close(self):
        try:
            if self.conn.is_connected():
                self.conn.close()
        except Exception:
            pass

    def execute(self, query: str, params=None) -> int:
        cur = self.conn.cursor()
        try:
            cur.execute(query, params)
            self.conn.commit()
            return cur.rowcount
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cur.close()

    def fetch_one(self, query: str, params=None):
        cur = self.conn.cursor()
        try:
            cur.execute(query, params)
            return cur.fetchone()
        finally:
            cur.close()

    def fetch_all(self, query: str, params=None):
        cur = self.conn.cursor()
        try:
            cur.execute(query, params)
            return cur.fetchall()
        finally:
            cur.close()
