import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config

# Get the project root directory (parent of backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DIST_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'dist')

app = Flask(__name__, static_folder=DIST_DIR, static_url_path='')
app.config.from_object(Config)

# Enable CORS for React frontend (dev mode)
CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

# Register blueprints
from routes.auth import auth_bp
from routes.topics import topics_bp
from routes.simulations import simulations_bp

app.register_blueprint(auth_bp)
app.register_blueprint(topics_bp)
app.register_blueprint(simulations_bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Cybersecurity Learning Platform API is running'
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    from utils.db import execute_query
    stats = {
        'total_users': execute_query("SELECT COUNT(*) as count FROM users", fetch_one=True)['count'],
        'total_topics': execute_query("SELECT COUNT(*) as count FROM topics", fetch_one=True)['count'],
        'total_simulations': len(simulations_bp.view_functions) - 1,
    }
    return jsonify(stats)

# Serve React app - catch-all route for client-side routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    # If the path is an API route, let Flask handle it (shouldn't reach here due to blueprints)
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    
    # Serve static files directly if they exist
    file_path = os.path.join(DIST_DIR, path)
    if path and os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(DIST_DIR, path)
    
    # Otherwise serve index.html for React Router
    return send_from_directory(DIST_DIR, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
