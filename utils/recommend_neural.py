from sentence_transformers import SentenceTransformer
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocessing import clean_text

class NeuralRecommender:
    def __init__(self, courses_file='data/cleaned_courses.csv'):
        # Load courses
        self.courses_df = pd.read_csv(courses_file)
        
        # Load precomputed embeddings (numpy array)
        self.embeddings = joblib.load('models/neural_embeddings.pkl')
        
        # Load SentenceTransformer object for query encoding
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # OR use joblib.load('models/sentence_transformer.pkl')
    
    def recommend(self, query, top_k=10):
        cleaned_query = clean_text(query)
        
        # Encode query using SentenceTransformer object
        query_embedding = self.model.encode([cleaned_query])
        
        # Compute cosine similarity
        similarities = cosine_similarity(query_embedding, self.embeddings).flatten()
        
        # Get top-k courses
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
