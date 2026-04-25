from flask import Blueprint, jsonify
from models import Topic, UserProgress, QuizResult
from routes.middleware import token_required

topics_bp = Blueprint('topics', __name__, url_prefix='/api/topics')

@topics_bp.route('/', methods=['GET'])
def get_topics():
    topics = Topic.get_all()
    return jsonify(topics)

@topics_bp.route('/<slug>', methods=['GET'])
def get_topic(slug):
    topic = Topic.get_by_slug(slug)
    if not topic:
        return jsonify({'error': 'Topic not found'}), 404
    return jsonify(topic)

@topics_bp.route('/progress', methods=['GET'])
@token_required
def get_progress(user_id):
    progress = UserProgress.get_user_progress(user_id)
    return jsonify(progress)

@topics_bp.route('/<int:topic_id>/progress', methods=['PUT'])
@token_required
def update_topic_progress(user_id, topic_id):
    from flask import request
    data = request.get_json()
    UserProgress.update_progress(
        user_id, 
        topic_id,
        completed=data.get('completed'),
        completion_percentage=data.get('completion_percentage'),
        simulations_completed=data.get('simulations_completed')
    )
    return jsonify({'message': 'Progress updated'})

@topics_bp.route('/quiz', methods=['POST'])
@token_required
def submit_quiz(user_id):
    from flask import request
    data = request.get_json()
    QuizResult.create(
        user_id,
        data['topic_id'],
        data['quiz_name'],
        data['score'],
        data['total_questions'],
        data.get('answers_json')
    )
    return jsonify({'message': 'Quiz result saved'}), 201

@topics_bp.route('/quiz-results', methods=['GET'])
@token_required
def get_quiz_results(user_id):
    results = QuizResult.get_user_quiz_results(user_id)
    return jsonify(results)
