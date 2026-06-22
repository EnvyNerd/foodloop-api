from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.bag_routes import bag_bp
from routes.order_routes import order_bp
from routes.vendor_routes import vendor_bp
from routes.notification_routes import notif_bp
from routes.user_routes import user_bp
import os

app = Flask(__name__)
CORS(app)

# Initialize DB if it doesn't exist
from config import DB_PATH
import sqlite3
if not os.path.exists(DB_PATH):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema_sqlite.sql")
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized")
    # Auto-seed on first deploy
    from seed import seed
    seed()

app.register_blueprint(auth_bp)
app.register_blueprint(bag_bp)
app.register_blueprint(order_bp)
app.register_blueprint(vendor_bp)
app.register_blueprint(notif_bp)
app.register_blueprint(user_bp)

@app.route("/")
def health():
    return jsonify({"status": "ok", "app": "FoodLoop API", "version": "1.6.0"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
