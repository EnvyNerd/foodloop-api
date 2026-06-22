from flask import Blueprint, request, jsonify
from models.vendor import Vendor
from models.payout import Payout
from models.user import User
from utils.auth_middleware import token_required

vendor_bp = Blueprint("vendor", __name__)

@vendor_bp.route("/vendor/stats", methods=["GET"])
@token_required
def get_stats():
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    v = Vendor.find_by_user_id(request.user["user_id"])
    if not v:
        return jsonify({"stats": {}}), 200
    stats = Vendor.get_stats(v["id"])
    return jsonify({"stats": stats}), 200

@vendor_bp.route("/vendor/profile", methods=["GET"])
@token_required
def get_profile():
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    v = Vendor.find_by_user_id(request.user["user_id"])
    if not v:
        return jsonify({"message": "Vendor profile not found"}), 404
    return jsonify({"vendor": v}), 200

@vendor_bp.route("/vendor/profile", methods=["PUT"])
@token_required
def update_profile():
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    v = Vendor.find_by_user_id(request.user["user_id"])
    if not v:
        return jsonify({"message": "Vendor profile not found"}), 404
    data = request.get_json()
    allowed = ["name", "address", "phone", "email", "hours", "lat", "lng"]
    updates = {k: v for k, v in data.items() if k in allowed}
    updated = Vendor.update(v["id"], updates)
    return jsonify({"vendor": updated}), 200

@vendor_bp.route("/vendor/payouts", methods=["GET"])
@token_required
def list_payouts():
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    v = Vendor.find_by_user_id(request.user["user_id"])
    if not v:
        return jsonify({"payouts": []}), 200
    payouts = Payout.list_by_vendor(v["id"])
    return jsonify({"payouts": payouts}), 200

@vendor_bp.route("/vendor/payouts/request", methods=["POST"])
@token_required
def request_payout():
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    v = Vendor.find_by_user_id(request.user["user_id"])
    if not v:
        return jsonify({"message": "Vendor profile not found"}), 404
    data = request.get_json()
    amount = float(data.get("amount", 0))
    if amount <= 0:
        return jsonify({"message": "Invalid amount"}), 400
    import time
    ref = f"BK-{int(time.time())}"
    payout = Payout.create(v["id"], amount, ref)
    return jsonify({"payout": payout}), 201

@vendor_bp.route("/vendors/<int:vendor_id>", methods=["GET"])
def get_vendor_public(vendor_id):
    v = Vendor.find_by_id(vendor_id)
    if not v:
        return jsonify({"message": "Vendor not found"}), 404
    return jsonify({"vendor": v}), 200
