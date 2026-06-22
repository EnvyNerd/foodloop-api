from flask import Blueprint, request, jsonify
from models.user import User
from models.vendor import Vendor

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role = data.get("role", "buyer")
    if not name or not email or not password:
        return jsonify({"message": "Name, email and password required"}), 400
    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400
    existing = User.find_by_email(email)
    if existing:
        return jsonify({"message": "Email already registered"}), 409
    user = User.create(name, email, password, role)
    token = User.generate_token({"id": user["id"], "email": email, "role": role})
    return jsonify({"token": token, "user": user}), 201

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400
    user = User.find_by_email(email)
    if not user or not User.verify_password(user, password):
        return jsonify({"message": "Invalid email or password"}), 401
    token = User.generate_token(user)
    resp = {"token": token, "user": {"id": user["id"], "name": user["name"], "email": user["email"], "role": user["role"]}}
    if user["role"] == "vendor":
        v = Vendor.find_by_user_id(user["id"])
        if v:
            resp["user"]["vendor_id"] = v["id"]
    return jsonify(resp), 200
