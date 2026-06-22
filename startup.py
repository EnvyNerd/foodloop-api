import os, sqlite3
from config import DB_PATH

# Initialize DB tables if fresh deploy
if not os.path.exists(DB_PATH):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema_sqlite.sql")
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized on fresh deploy")

# Import and run seed if DB is empty
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
count = conn.execute("SELECT COUNT(*) as cnt FROM users").fetchone()["cnt"]
conn.close()

if count == 0:
    print("Seeding database with test data...")
    from seed import seed
    seed()
    print("Seeding complete!")
else:
    print(f"Database already has {count} users, skipping seed")
