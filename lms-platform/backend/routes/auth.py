from flask import Blueprint, request, jsonify
from models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    
    if not all([username, email, password]):
        return jsonify({'error': 'Username, email, and password are required'}), 400
    
    # Check if user exists
    if User.get_by_email(email):
        return jsonify({'error': 'Email already registered'}), 409
    
    try:
        user_id = User.create(username, email, password, full_name)
        token = User.generate_token(user_id)
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {'id': user_id, 'username': username, 'email': email}
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = User.get_by_email(email)
    if not user or not User.verify_password(user, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = User.generate_token(user['id'])
    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'full_name': user['full_name'],
            'role': user['role']
        }
    })

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    from routes.middleware import token_required
    return token_required(lambda user_id: jsonify(User.get_by_id(user_id)))()
