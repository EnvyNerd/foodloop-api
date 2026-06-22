from functools import wraps
from flask import request, jsonify
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth = request.headers["Authorization"]
            if auth.startswith("Bearer "):
                token = auth[7:]
        if not token:
            return jsonify({"message": "Token missing"}), 401
        payload = User.decode_token(token)
        if not payload:
            return jsonify({"message": "Token invalid or expired"}), 401
        request.user = payload
        return f(*args, **kwargs)
    return decorated

def vendor_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user.get("role") != "vendor":
            return jsonify({"message": "Vendor access required"}), 403
        return f(*args, **kwargs)
    return decorated
