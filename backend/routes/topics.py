from flask import Blueprint, jsonify, send_from_directory
from models import Topic, UserProgress, QuizResult
from routes.middleware import token_required
import os
import markdown as md_lib

topics_bp = Blueprint('topics', __name__, url_prefix='/api/topics')

# Map topic slugs to their folder names for README lookup
SLUG_TO_FOLDER = {
    'intro-to-cybersecurity': '1. Intro to cybersecurity',
    'networking-fundamentals': '2. Networking Fundamentals',
    'operating-systems-security': '3. Operating system and security',
    'cryptography': '4. Cryptography',
    'web-application-security': '5. Web Application Security',
    'network-security': '6. Network Security',
    'security-assessment-testing': '7. Security Assessment and Testing',
    'incident-response-forensics': '8. Incident Response and Forensics',
    'cloud-security': '9. Cloud Security',
    'mobile-security': '10. Mobile Security',
    'threat-intelligence': '11. Threat Intelligence and Security Analytics',
    'ics-security': '12. Industrial Control Systems Security',
    'advanced-persistent-threats': '13. Advanced Persistent Threats',
    'secure-software-development': '14. Secure Software Development',
    'emerging-technologies': '15. Emerging Technologies in Cybersecurity',
}


def markdown_to_html(text):
    """Convert markdown to HTML using the markdown library with extensions."""
    extensions = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
    ]
    return md_lib.markdown(text, extensions=extensions)


@topics_bp.route('/', methods=['GET'])
def get_topics():
    topics = Topic.get_all()
    return jsonify(topics)


@topics_bp.route('/<slug>/content', methods=['GET'])
def get_topic_content(slug):
    """Fetch the topic's README.md and return as HTML."""
    if slug not in SLUG_TO_FOLDER:
        return jsonify({'error': 'Topic folder not found'}), 404
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    folder = SLUG_TO_FOLDER[slug]
    readme_path = os.path.join(base_dir, folder, 'README.md')
    
    if not os.path.exists(readme_path):
        return jsonify({'error': 'README not found'}), 404
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        html_content = markdown_to_html(markdown_content)
        return jsonify({
            'slug': slug,
            'html': html_content,
            'markdown': markdown_content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
