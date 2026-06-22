import sqlite3, random, string, os
from config import DB_PATH, SECRET_KEY
from werkzeug.security import generate_password_hash

def seed():
    # Remove old DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Create tables
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "schema_sqlite.sql")
    with open(schema_path, "r") as f:
        conn.executescript(f.read())

    # Seed users
    users = [
        ("Admin", "admin@foodloop.my", "admin123", "admin"),
        ("Witschi", "witschi@email.com", "password123", "buyer"),
        ("Ahmad Nabil", "ahmad@email.com", "password123", "buyer"),
        ("Siti Rahimah", "siti@email.com", "password123", "buyer"),
        ("Sunrise Bakery", "restaurant0@foodloop.my", "password123", "vendor"),
        ("Kopi Senja Cafe", "restaurant1@foodloop.my", "password123", "vendor"),
    ]
    user_ids = []
    for name, email, pwd, role in users:
        h = generate_password_hash(pwd, method="pbkdf2:sha256")
        cur = conn.execute("INSERT INTO users (name,email,password_hash,role) VALUES (?,?,?,?)", (name, email, h, role))
        user_ids.append(cur.lastrowid)

    # Seed vendors
    vendors = [
        (5, "Sunrise Bakery", "Jalan Dunlop, Tawau, Sabah", "+6012-345-6789", "hello@sunrisebakery.my", "Mon-Sat 7AM-9PM, Sun 8AM-6PM", 4.2985, 117.8831, 4.2, 138),
        (6, "Kopi Senja Cafe", "Jalan Habib Hussein, Tawau, Sabah", "+6012-456-7890", "hello@kopisenja.my", "Daily 8AM-10PM", 4.2960, 117.8900, 4.5, 92),
    ]
    vendor_ids = []
    for uid, name, addr, phone, email, hours, lat, lng, rating, reviews in vendors:
        cur = conn.execute("INSERT INTO vendors (user_id,name,address,phone,email,hours,lat,lng,rating,review_count) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (uid, name, addr, phone, email, hours, lat, lng, rating, reviews))
        vendor_ids.append(cur.lastrowid)

    # Seed bags
    bags_data = [
        (1, "Sunrise Bakery Surprise Bag", "A surprise selection of today's fresh leftovers.", "Bread, pastries, buns", "Bakery", "halal", 6, 18, "19:30", "20:30", "Jalan Dunlop, Tawau, Sabah", 10, "Vegetarian-friendly,No nuts", None, 4.2985, 117.8831),
        (1, "Morning Pastry Box", "Assorted pastries from this morning's batch.", "Croissants, danishes, muffins", "Bakery", "halal", 8, 20, "18:00", "19:00", "Jalan Dunlop, Tawau, Sabah", 8, "Fresh today,No nuts", None, 4.2985, 117.8831),
        (2, "Kopi Senja Cafe Bag", "Mix of today's cafe drinks and light bites.", "Kuih, sandwiches, 1 bottled drink", "Cafe", "halal", 8, 22, "20:00", "21:00", "Jalan Habib Hussein, Tawau, Sabah", 10, "Vegetarian options,Drinks included", None, 4.2960, 117.8900),
        (2, "Evening Kuih Box", "Traditional Malay kuih from today's batch.", "Kuih-muih assorted, roti", "Cafe", "halal", 5, 15, "17:00", "18:00", "Jalan Habib Hussein, Tawau, Sabah", 12, "Traditional,Halal certified", None, 4.2960, 117.8900),
    ]
    bag_ids = []
    for vid, name, desc, contents, cat, halal, pn, ps, pstart, pend, addr, qt, tags, img, lat, lng in bags_data:
        cur = conn.execute("INSERT INTO bags (vendor_id,name,description,contents,category,halal,price_now,price_original,pickup_start,pickup_end,pickup_address,quantity_total,quantity_left,tags,image_url,lat,lng) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (vid, name, desc, contents, cat, halal, pn, ps, pstart, pend, addr, qt, qt, tags, img, lat, lng))
        bag_ids.append(cur.lastrowid)

    # Seed orders
    for i in range(5):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        buyer = random.choice([2, 3, 4])
        bag_id = random.choice(bag_ids)
        vendor_id = 1 if bag_id <= 2 else 2
        price = {1:6, 2:8, 3:8, 4:5}[bag_id]
        status = random.choice(["paid", "ready", "collected"])
        conn.execute("INSERT INTO orders (bag_id,buyer_id,vendor_id,price,status,pickup_code) VALUES (?,?,?,?,?,?)",
            (bag_id, buyer, vendor_id, price, status, code))

    # Seed payouts
    for vid, amt, status, ref in [(1,245.70,"completed","BK-20260615-001"),(1,198.40,"completed","BK-20260601-001"),(2,312.80,"completed","BK-20260515-001")]:
        conn.execute("INSERT INTO payouts (vendor_id,amount,status,reference) VALUES (?,?,?,?)", (vid, amt, status, ref))

    conn.commit()
    conn.close()
    print("Seeding complete!")

if __name__ == "__main__":
    seed()
