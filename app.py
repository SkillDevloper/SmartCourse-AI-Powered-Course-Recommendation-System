from flask import Flask, render_template, request, jsonify, session
import sqlite3
import json
from datetime import datetime
from utils.recommend_tfidf import TFIDFRecommender
from utils.recommend_neural import NeuralRecommender

app = Flask(__name__)
app.secret_key = 'smartcourse_secret_key_2024'

# Initialize recommenders
tfidf_recommender = TFIDFRecommender()
neural_recommender = NeuralRecommender()

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend')
def recommend_page():
    return render_template('recommend.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        model_type = data.get('model', 'tfidf')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Get recommendations based on model type
        if model_type == 'tfidf':
            recommendations = tfidf_recommender.recommend(query)
        else:
            recommendations = neural_recommender.recommend(query)
        
        # Save to search history
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO history (query_text, model_type, user_id) VALUES (?, ?, ?)',
            (query, model_type, 1)  # Using demo user for now
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'query': query,
            'model': model_type,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        conn = get_db_connection()
        history = conn.execute('''
            SELECT query_text, model_type, timestamp 
            FROM history 
            WHERE user_id = 1 
            ORDER BY timestamp DESC 
            LIMIT 50
        ''').fetchall()
        conn.close()
        
        history_list = []
        for item in history:
            history_list.append({
                'query_text': item['query_text'],
                'model_type': item['model_type'],
                'timestamp': item['timestamp']
            })
        
        return jsonify({'history': history_list})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def save_course():
    try:
        data = request.get_json()
        course_name = data.get('course_name')
        department = data.get('department')
        description = data.get('description')
        model_type = data.get('model_type')
        query_text = data.get('query_text')
        
        conn = get_db_connection()
        conn.execute(
            '''INSERT INTO saved_courses 
               (course_name, department, description, model_type, query_text, user_id) 
               VALUES (?, ?, ?, ?, ?, ?)''',
            (course_name, department, description, model_type, query_text, 1)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Course saved successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/saved-courses', methods=['GET'])
def get_saved_courses():
    try:
        conn = get_db_connection()
        saved_courses = conn.execute('''
            SELECT course_name, department, description, model_type, query_text, timestamp
            FROM saved_courses 
            WHERE user_id = 1 
            ORDER BY timestamp DESC
        ''').fetchall()
        conn.close()
        
        courses_list = []
        for course in saved_courses:
            courses_list.append({
                'course_name': course['course_name'],
                'department': course['department'],
                'description': course['description'],
                'model_type': course['model_type'],
                'query_text': course['query_text'],
                'timestamp': course['timestamp']
            })
        
        return jsonify({'saved_courses': courses_list})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)