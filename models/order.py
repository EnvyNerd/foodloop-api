import sqlite3, random, string
from config import DB_PATH

class Order:
    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _pickup_code():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    @staticmethod
    def create(bag_id, buyer_id, vendor_id, price):
        conn = Order._conn()
        code = Order._pickup_code()
        cur = conn.execute("INSERT INTO orders (bag_id,buyer_id,vendor_id,price,status,pickup_code) VALUES (?,?,?,?,?,?)",
            (bag_id, buyer_id, vendor_id, price, "paid", code))
        conn.commit()
        oid = cur.lastrowid
        row = conn.execute("SELECT * FROM orders WHERE id=?", (oid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def find_by_id(oid):
        conn = Order._conn()
        row = conn.execute("SELECT o.*, b.name as bag_name, b.vendor FROM orders o JOIN bags b ON o.bag_id=b.id WHERE o.id=?", (oid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def list_by_buyer(uid):
        conn = Order._conn()
        rows = conn.execute("SELECT o.*, b.name as bag_name, b.vendor FROM orders o JOIN bags b ON o.bag_id=b.id WHERE o.buyer_id=? ORDER BY o.created_at DESC", (uid,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def list_by_vendor(vid):
        conn = Order._conn()
        rows = conn.execute("SELECT o.*, b.name as bag_name, u.name as buyer_name FROM orders o JOIN bags b ON o.bag_id=b.id JOIN users u ON o.buyer_id=u.id WHERE o.vendor_id=? ORDER BY o.created_at DESC", (vid,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def update_status(oid, new_status):
        conn = Order._conn()
        conn.execute("UPDATE orders SET status=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (new_status, oid))
        conn.commit()
        row = conn.execute("SELECT * FROM orders WHERE id=?", (oid,)).fetchone()
        conn.close()
        return dict(row) if row else None
