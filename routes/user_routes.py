from flask import Blueprint, request, jsonify
from models.user import User
from utils.auth_middleware import token_required

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/profile", methods=["GET"])
@token_required
def get_profile():
    user = User.find_by_id(request.user["user_id"])
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"profile": user}), 200

@user_bp.route("/user/profile", methods=["PUT"])
@token_required
def update_profile():
    data = request.get_json()
    # In production, update user in DB
    return jsonify({"profile": {"id": request.user["user_id"], "name": data.get("name", ""), "email": request.user["email"], "role": request.user["role"]}}), 200
