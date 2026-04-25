from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for React frontend
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
        'total_simulations': len(simulations_bp.view_functions) - 1,  # Exclude list
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
