# File: utils/recommend_tfidf.py
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocessing import clean_text

class TFIDFRecommender:
    def __init__(self, courses_file='data/cleaned_courses.csv'):
        self.courses_df = pd.read_csv(courses_file)
        self.tfidf_matrix = joblib.load('models/tfidf_model.joblib')
        self.vectorizer = joblib.load('models/tfidf_vectorizer.joblib')
    
    def recommend(self, query, top_k=10):
        """Get recommendations using TF-IDF and cosine similarity"""
        # Clean query
        cleaned_query = clean_text(query)
        
        # Transform query to TF-IDF
        query_vector = self.vectorizer.transform([cleaned_query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top k recommendations
        top_indices = np.argsort(similarities)[::-1][:top_k]
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0:
                course = self.courses_df.iloc[idx]
                recommendations.append({
                    'course_name': course['course_name'],
                    'university': course['university'],
                    'department': course['department'],
                    'difficulty': course['difficulty'],
                    'rating': course['rating'],
                    'description': course['description'],
                    'score': float(similarities[idx]),
                    'score_percentage': min(100, float(similarities[idx]) * 100)
                })
        
        return recommendations
