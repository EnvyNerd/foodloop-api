import sqlite3
from config import DB_PATH

class Vendor:
    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def create(user_id, name, address, phone=None, email=None, hours=None, lat=None, lng=None):
        conn = Vendor._conn()
        cur = conn.execute("INSERT INTO vendors (user_id,name,address,phone,email,hours,lat,lng) VALUES (?,?,?,?,?,?,?,?)",
            (user_id, name, address, phone, email, hours, lat, lng))
        conn.commit()
        vid = cur.lastrowid
        conn.close()
        return {"id": vid, "user_id": user_id, "name": name, "address": address, "phone": phone, "email": email, "hours": hours, "lat": lat, "lng": lng, "rating": 0, "review_count": 0}

    @staticmethod
    def find_by_user_id(uid):
        conn = Vendor._conn()
        row = conn.execute("SELECT * FROM vendors WHERE user_id=?", (uid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def find_by_id(vid):
        conn = Vendor._conn()
        row = conn.execute("SELECT * FROM vendors WHERE id=?", (vid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(vid, updates):
        conn = Vendor._conn()
        fields = ", ".join(f"{k}=?" for k in updates)
        conn.execute(f"UPDATE vendors SET {fields} WHERE id=?", list(updates.values()) + [vid])
        conn.commit()
        row = conn.execute("SELECT * FROM vendors WHERE id=?", (vid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_stats(vid):
        conn = Vendor._conn()
        today = conn.execute("SELECT COUNT(*) as sold, COALESCE(SUM(price),0) as earnings FROM orders WHERE vendor_id=? AND date(created_at)=date('now') AND status IN ('paid','ready','collected')", (vid,)).fetchone()
        month = conn.execute("SELECT COUNT(*) as sold, COALESCE(SUM(price),0) as earnings FROM orders WHERE vendor_id=? AND strftime('%Y-%m',created_at)=strftime('%Y-%m','now') AND status IN ('paid','ready','collected')", (vid,)).fetchone()
        remaining = conn.execute("SELECT COALESCE(SUM(quantity_left),0) as remaining FROM bags WHERE vendor_id=? AND active=1", (vid,)).fetchone()
        rating = conn.execute("SELECT rating, review_count FROM vendors WHERE id=?", (vid,)).fetchone()
        conn.close()
        return {"today_sold": today["sold"], "today_earnings": float(today["earnings"] or 0),
                "month_sold": month["sold"], "month_earnings": float(month["earnings"] or 0),
                "today_remaining": remaining["remaining"], "sellThroughRate": 0,
                "avgRating": float(rating["rating"] or 0), "totalReviews": rating["review_count"] or 0,
                "monthFoodRescued": month["sold"], "monthCO2Saved": month["sold"] * 2}
