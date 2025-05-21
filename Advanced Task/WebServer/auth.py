from functools import wraps
from flask import request, jsonify
from data import ADMIN_TOKEN

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('X-Admin-Token')
        if not token or token != ADMIN_TOKEN:
            return jsonify({"error": "Unauthorized: Admin token missing or invalid"}), 401
        return f(*args, **kwargs)
    return decorated_function