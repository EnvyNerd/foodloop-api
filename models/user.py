import sqlite3, jwt, datetime
from config import DB_PATH, SECRET_KEY, JWT_EXPIRATION_HOURS
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def create(name, email, password, role="buyer"):
        conn = User._conn()
        hashed = generate_password_hash(password, method="pbkdf2:sha256")
        cur = conn.execute("INSERT INTO users (name, email, password_hash, role) VALUES (?,?,?,?)", (name, email, hashed, role))
        conn.commit()
        uid = cur.lastrowid
        conn.close()
        return {"id": uid, "name": name, "email": email, "role": role}

    @staticmethod
    def find_by_email(email):
        conn = User._conn()
        row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def find_by_id(uid):
        conn = User._conn()
        row = conn.execute("SELECT id, name, email, role, created_at FROM users WHERE id=?", (uid,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user["password_hash"], password)

    @staticmethod
    def generate_token(user):
        payload = {"user_id": user["id"], "email": user["email"], "role": user["role"],
                   "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)}
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except: return None
