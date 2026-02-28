import spacy
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
import joblib

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Please download the spaCy model first:")
    print("python -m spacy download en_core_web_sm")
    nlp = None

def clean_text(text):
    """Clean and preprocess text using spaCy"""
    if pd.isna(text):
        return ""
    
    # Remove HTML tags and special characters
    text = re.sub(r'<[^>]+>', '', str(text))
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower().strip()
    
    if nlp:
        doc = nlp(text)
        # Lemmatize and remove stopwords
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return ' '.join(tokens)
    else:
        # Fallback simple cleaning
        return text

def prepare_tfidf_model(courses_df):
    """Create and save TF-IDF model"""
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8
    )
    
    tfidf_matrix = vectorizer.fit_transform(courses_df['cleaned_description'])
    
    # Save model and vectorizer
    joblib.dump(tfidf_matrix, 'models/tfidf_model.joblib')
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.joblib')
    
    return tfidf_matrix, vectorizer

def prepare_neural_embeddings(courses_df):
    """Create and save neural embeddings"""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(courses_df['cleaned_description'].tolist())
    
    # Save embeddings
    joblib.dump(embeddings, 'models/neural_embeddings.pkl')
    joblib.dump(model, 'models/sentence_transformer.pkl')
    
    return embeddings, model