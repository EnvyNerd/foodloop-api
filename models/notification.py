import sqlite3
from config import DB_PATH

class Notification:
    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def create(user_id, title, message, notif_type):
        conn = Notification._conn()
        cur = conn.execute("INSERT INTO notifications (user_id,title,message,type) VALUES (?,?,?,?)", (user_id, title, message, notif_type))
        conn.commit()
        nid = cur.lastrowid
        conn.close()
        return {"id": nid, "user_id": user_id, "title": title, "message": message, "type": notif_type, "read": 0}

    @staticmethod
    def list_by_user(uid):
        conn = Notification._conn()
        rows = conn.execute("SELECT * FROM notifications WHERE user_id=? ORDER BY created_at DESC LIMIT 50", (uid,)).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def mark_read(nid, uid):
        conn = Notification._conn()
        conn.execute("UPDATE notifications SET read=1 WHERE id=? AND user_id=?", (nid, uid))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def mark_all_read(uid):
        conn = Notification._conn()
        conn.execute("UPDATE notifications SET read=1 WHERE user_id=?", (uid,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def unread_count(uid):
        conn = Notification._conn()
        row = conn.execute("SELECT COUNT(*) as cnt FROM notifications WHERE user_id=? AND read=0", (uid,)).fetchone()
        conn.close()
        return row["cnt"]
