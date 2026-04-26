from utils.db import execute_query
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from config import Config

class User:
    @staticmethod
    def create(username, email, password, full_name=None):
        password_hash = generate_password_hash(password)
        query = """
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (%s, %s, %s, %s)
        """
        user_id = execute_query(query, (username, email, password_hash, full_name))
        
        # Initialize progress for all topics
        topics = execute_query("SELECT id FROM topics")
        for topic in topics:
            execute_query(
                "INSERT INTO user_progress (user_id, topic_id) VALUES (%s, %s)",
                (user_id, topic['id'])
            )
        return user_id

    @staticmethod
    def get_by_email(email):
        return execute_query("SELECT * FROM users WHERE email = %s", (email,), fetch_one=True)

    @staticmethod
    def get_by_id(user_id):
        return execute_query("SELECT id, username, email, full_name, role, created_at FROM users WHERE id = %s", 
                           (user_id,), fetch_one=True)

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user['password_hash'], password)

    @staticmethod
    def generate_token(user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

class Topic:
    @staticmethod
    def get_all():
        return execute_query("SELECT * FROM topics ORDER BY order_num")

    @staticmethod
    def get_by_slug(slug):
        return execute_query("SELECT * FROM topics WHERE slug = %s", (slug,), fetch_one=True)

    @staticmethod
    def get_by_id(topic_id):
        return execute_query("SELECT * FROM topics WHERE id = %s", (topic_id,), fetch_one=True)

class UserProgress:
    @staticmethod
    def get_user_progress(user_id):
        query = """
            SELECT up.*, t.title, t.slug, t.description, t.icon
            FROM user_progress up
            JOIN topics t ON up.topic_id = t.id
            WHERE up.user_id = %s
            ORDER BY t.order_num
        """
        return execute_query(query, (user_id,))

    @staticmethod
    def update_progress(user_id, topic_id, completed=None, completion_percentage=None, simulations_completed=None):
        fields = []
        params = []
        if completed is not None:
            fields.append("completed = %s")
            params.append(completed)
        if completion_percentage is not None:
            fields.append("completion_percentage = %s")
            params.append(completion_percentage)
        if simulations_completed is not None:
            fields.append("simulations_completed = %s")
            params.append(simulations_completed)
        fields.append("last_accessed = NOW()")
        
        query = f"UPDATE user_progress SET {', '.join(fields)} WHERE user_id = %s AND topic_id = %s"
        params.extend([user_id, topic_id])
        execute_query(query, tuple(params))

class QuizResult:
    @staticmethod
    def create(user_id, topic_id, quiz_name, score, total_questions, answers_json=None):
        query = """
            INSERT INTO quiz_results (user_id, topic_id, quiz_name, score, total_questions, answers_json)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (user_id, topic_id, quiz_name, score, total_questions, answers_json))
        
        # Update user progress average score
        avg_query = """
            UPDATE user_progress 
            SET avg_quiz_score = (
                SELECT AVG(score / total_questions * 100) 
                FROM quiz_results 
                WHERE user_id = %s AND topic_id = %s
            ),
            quizzes_taken = quizzes_taken + 1
            WHERE user_id = %s AND topic_id = %s
        """
        execute_query(avg_query, (user_id, topic_id, user_id, topic_id))

    @staticmethod
    def get_user_quiz_results(user_id, topic_id=None):
        if topic_id:
            return execute_query(
                "SELECT * FROM quiz_results WHERE user_id = %s AND topic_id = %s ORDER BY taken_at DESC",
                (user_id, topic_id)
            )
        return execute_query(
            "SELECT * FROM quiz_results WHERE user_id = %s ORDER BY taken_at DESC",
            (user_id,)
        )

class SimulationLog:
    @staticmethod
    def create(user_id, topic_id, simulation_name, input_params=None, result_summary=None, result_json=None, execution_time_ms=None):
        query = """
            INSERT INTO simulation_logs 
            (user_id, topic_id, simulation_name, input_params, result_summary, result_json, execution_time_ms)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (user_id, topic_id, simulation_name, input_params, result_summary, result_json, execution_time_ms))

    @staticmethod
    def get_user_simulations(user_id, topic_id=None):
        if topic_id:
            return execute_query(
                "SELECT * FROM simulation_logs WHERE user_id = %s AND topic_id = %s ORDER BY executed_at DESC",
                (user_id, topic_id)
            )
        return execute_query(
            "SELECT * FROM simulation_logs WHERE user_id = %s ORDER BY executed_at DESC",
            (user_id,)
        )
