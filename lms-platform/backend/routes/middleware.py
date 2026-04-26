from functools import wraps
from flask import request, jsonify
from models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        user_id = User.verify_token(token)
        if not user_id:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        return f(user_id, *args, **kwargs)
    return decorated
