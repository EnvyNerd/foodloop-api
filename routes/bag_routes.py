from flask import Blueprint, request, jsonify
from models.bag import Bag
from utils.auth_middleware import token_required

bag_bp = Blueprint("bags", __name__)

@bag_bp.route("/bags", methods=["GET"])
def list_bags():
    filters = {}
    if request.args.get("category"):
        filters["category"] = request.args.get("category")
    if request.args.get("halal"):
        filters["halal"] = request.args.get("halal")
    if request.args.get("search"):
        filters["search"] = request.args.get("search")
    if request.args.get("vendor_id"):
        filters["vendor_id"] = int(request.args.get("vendor_id"))
    bags = Bag.list_all(filters)
    return jsonify({"bags": bags}), 200

@bag_bp.route("/bags/<int:bag_id>", methods=["GET"])
def get_bag(bag_id):
    bag = Bag.find_by_id(bag_id)
    if not bag:
        return jsonify({"message": "Bag not found"}), 404
    return jsonify({"bag": bag}), 200

@bag_bp.route("/vendor/bags", methods=["POST"])
@token_required
def create_bag():
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    from models.vendor import Vendor
    v = Vendor.find_by_user_id(request.user["user_id"])
    if not v:
        return jsonify({"message": "Create a vendor profile first"}), 400
    data = request.get_json()
    required = ["name", "description", "contents", "price_now", "price_original", "pickup_start", "pickup_end", "quantity_total"]
    for f in required:
        if not data.get(f):
            return jsonify({"message": f"{f} is required"}), 400
    bag = Bag.create(
        vendor_id=v["id"], name=data["name"], description=data["description"],
        contents=data["contents"], category=data.get("category","Bakery"),
        halal=data.get("halal","halal"), price_now=float(data["price_now"]),
        price_original=float(data["price_original"]), pickup_start=data["pickup_start"],
        pickup_end=data["pickup_end"], pickup_address=data.get("pickup_address",""),
        quantity_total=int(data["quantity_total"]), tags=data.get("tags",""),
        image_url=data.get("image_url"), lat=data.get("lat"), lng=data.get("lng")
    )
    return jsonify({"bag": bag}), 201

@bag_bp.route("/vendor/bags/<int:bag_id>", methods=["PUT"])
@token_required
def update_bag(bag_id):
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    data = request.get_json()
    bag = Bag.update(bag_id, data)
    return jsonify({"bag": bag}), 200

@bag_bp.route("/vendor/bags/<int:bag_id>", methods=["DELETE"])
@token_required
def delete_bag(bag_id):
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    Bag.delete(bag_id)
    return jsonify({"success": True}), 200

@bag_bp.route("/vendor/bags/<int:bag_id>/toggle", methods=["PATCH"])
@token_required
def toggle_bag(bag_id):
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    data = request.get_json()
    bag = Bag.update(bag_id, {"active": data.get("active", True)})
    return jsonify({"bag": bag}), 200

@bag_bp.route("/vendor/products", methods=["GET"])
@token_required
def list_vendor_products():
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    from models.vendor import Vendor
    v = Vendor.find_by_user_id(request.user["user_id"])
    if not v:
        return jsonify({"products": []}), 200
    bags = Bag.list_all({"vendor_id": v["id"]})
    return jsonify({"products": bags}), 200
