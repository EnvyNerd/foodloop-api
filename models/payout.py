import sqlite3
from config import DB_PATH

class Payout:
    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def create(vendor_id, amount, reference):
        conn = Payout._conn()
        cur = conn.execute("INSERT INTO payouts (vendor_id,amount,status,reference) VALUES (?,?,?,?)", (vendor_id, amount, "pending", reference))
        conn.commit()
        pid = cur.lastrowid
        conn.close()
        return {"id": pid, "vendor_id": vendor_id, "amount": amount, "status": "pending", "reference": reference}

    @staticmethod
    def list_by_vendor(vid):
        conn = Payout._conn()
        rows = conn.execute("SELECT * FROM payouts WHERE vendor_id=? ORDER BY created_at DESC", (vid,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]
