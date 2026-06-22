from flask import Blueprint, request, jsonify
from models.order import Order
from models.bag import Bag
from models.notification import Notification
from models.vendor import Vendor
from utils.auth_middleware import token_required

order_bp = Blueprint("orders", __name__)

@order_bp.route("/orders", methods=["POST"])
@token_required
def create_order():
    data = request.get_json()
    bag_id = data.get("bag_id")
    if not bag_id:
        return jsonify({"message": "bag_id required"}), 400
    bag = Bag.find_by_id(bag_id)
    if not bag:
        return jsonify({"message": "Bag not found"}), 404
    if bag["quantity_left"] <= 0:
        return jsonify({"message": "No bags remaining"}), 400
    v = Vendor.find_by_id(bag["vendor_id"])
    order = Order.create(bag_id=bag_id, buyer_id=request.user["user_id"], vendor_id=v["id"], price=bag["price_now"])
    Bag.decrement_quantity(bag_id)
    # Notify vendor
    Notification.create(user_id=v["user_id"], title=f"New order: {order['id']}", message=f"A customer reserved {bag['name']} for RM {bag['price_now']}", notif_type="order_placed")
    return jsonify({"order": order}), 201

@order_bp.route("/orders", methods=["GET"])
@token_required
def list_orders():
    orders = Order.list_by_buyer(request.user["user_id"])
    return jsonify({"orders": orders}), 200

@order_bp.route("/orders/<int:order_id>", methods=["GET"])
@token_required
def get_order(order_id):
    order = Order.find_by_id(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404
    return jsonify({"order": order}), 200

@order_bp.route("/orders/<int:order_id>/status", methods=["PATCH"])
@token_required
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ("paid", "ready", "collected", "cancelled"):
        return jsonify({"message": "Invalid status"}), 400
    order = Order.update_status(order_id, new_status)
    # Generate notifications based on status
    if new_status == "ready":
        Notification.create(user_id=order["buyer_id"], title="Your order is ready!", message=f"{order['bag_name']} is ready for pickup. Don't forget your pickup code!", notif_type="order_ready")
    elif new_status == "collected":
        Notification.create(user_id=order["buyer_id"], title="Order collected!", message=f"Order {order['id']} collected. Thank you for saving food!", notif_type="order_collected")
    return jsonify({"order": order}), 200

@order_bp.route("/vendor/orders", methods=["GET"])
@token_required
def list_vendor_orders():
    if request.user.get("role") != "vendor":
        return jsonify({"message": "Vendor access required"}), 403
    v = Vendor.find_by_user_id(request.user["user_id"])
    if not v:
        return jsonify({"orders": []}), 200
    orders = Order.list_by_vendor(v["id"])
    return jsonify({"orders": orders}), 200
