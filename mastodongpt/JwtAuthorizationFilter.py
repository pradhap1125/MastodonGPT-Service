import time

from flask import request, jsonify
from mastodongpt.JwtService import decode_unsigned_jwt
from mastodongpt.DbService import validate_userName
from functools import wraps

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]
        jwt_data = decode_unsigned_jwt(token)

        if not jwt_data:
            return jsonify({"error": "Invalid JWT"}), 401

        if 'sub' not in jwt_data['payload']:
            return jsonify({"error": "Invalid JWT payload"}), 403

        if not validate_userName(jwt_data['payload']['name']):
            return jsonify({"error": "Invalid user"}), 403

        if jwt_data['payload']["iat"] + 60 * 60 < int(time.time()):
            return jsonify({"error": "JWT expired"}), 403

        request.jwt_payload = jwt_data['payload']
        return f(*args, **kwargs)
    return decorated


