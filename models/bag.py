import sqlite3
from config import DB_PATH

class Bag:
    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def create(vendor_id, name, description, contents, category, halal, price_now, price_original, pickup_start, pickup_end, pickup_address, quantity_total, tags=None, image_url=None, lat=None, lng=None):
        conn = Bag._conn()
        cur = conn.execute("INSERT INTO bags (vendor_id,name,description,contents,category,halal,price_now,price_original,pickup_start,pickup_end,pickup_address,quantity_total,quantity_left,tags,image_url,lat,lng) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (vendor_id, name, description, contents, category, halal, price_now, price_original, pickup_start, pickup_end, pickup_address, quantity_total, quantity_total, tags, image_url, lat, lng))
        conn.commit()
        bid = cur.lastrowid
        conn.close()
        return Bag.find_by_id(bid)

    @staticmethod
    def find_by_id(bid):
        conn = Bag._conn()
        row = conn.execute("SELECT b.*, v.name as vendor FROM bags b JOIN vendors v ON b.vendor_id=v.id WHERE b.id=?", (bid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def list_all(filters=None):
        conn = Bag._conn()
        query = "SELECT b.*, v.name as vendor FROM bags b JOIN vendors v ON b.vendor_id=v.id WHERE b.active=1 AND b.quantity_left>0"
        params = []
        if filters:
            if filters.get("category"): query += " AND b.category=?"; params.append(filters["category"])
            if filters.get("halal"): query += " AND b.halal=?"; params.append(filters["halal"])
            if filters.get("search"): query += " AND (b.name LIKE ? OR v.name LIKE ?)"; params.extend([f"%{filters['search']}%", f"%{filters['search']}%"])
            if filters.get("vendor_id"): query += " AND b.vendor_id=?"; params.append(filters["vendor_id"])
        query += " ORDER BY b.created_at DESC"
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def update(bid, updates):
        conn = Bag._conn()
        fields = ", ".join(f"{k}=?" for k in updates)
        conn.execute(f"UPDATE bags SET {fields} WHERE id=?", list(updates.values()) + [bid])
        conn.commit()
        row = conn.execute("SELECT * FROM bags WHERE id=?", (bid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def delete(bid):
        conn = Bag._conn()
        conn.execute("DELETE FROM bags WHERE id=?", (bid,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def decrement_quantity(bid):
        conn = Bag._conn()
        conn.execute("UPDATE bags SET quantity_left=quantity_left-1 WHERE id=? AND quantity_left>0", (bid,))
        conn.commit()
        conn.close()
