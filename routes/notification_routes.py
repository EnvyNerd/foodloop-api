from flask import Blueprint, request, jsonify
from models.notification import Notification
from utils.auth_middleware import token_required

notif_bp = Blueprint("notifications", __name__)

@notif_bp.route("/notifications", methods=["GET"])
@token_required
def list_notifications():
    notifs = Notification.list_by_user(request.user["user_id"])
    return jsonify({"notifications": notifs}), 200

@notif_bp.route("/notifications/<int:notif_id>/read", methods=["PATCH"])
@token_required
def mark_read(notif_id):
    Notification.mark_read(notif_id, request.user["user_id"])
    return jsonify({"success": True}), 200

@notif_bp.route("/notifications/read-all", methods=["PATCH"])
@token_required
def mark_all_read():
    Notification.mark_all_read(request.user["user_id"])
    return jsonify({"success": True}), 200

@notif_bp.route("/notifications/unread-count", methods=["GET"])
@token_required
def unread_count():
    count = Notification.unread_count(request.user["user_id"])
    return jsonify({"count": count}), 200
