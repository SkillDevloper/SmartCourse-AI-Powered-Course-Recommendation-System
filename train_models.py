import os
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer

# Load cleaned course descriptions
df = pd.read_csv('data/cleaned_courses.csv')
corpus = df['cleaned_description'].astype(str).tolist()

# Ensure models folder exists
if not os.path.exists('models'):
    os.makedirs('models')

# ---- TF-IDF Model ----
tfidf = TfidfVectorizer(ngram_range=(1,2))
tfidf_matrix = tfidf.fit_transform(corpus)

joblib.dump(tfidf, 'models/tfidf_vectorizer.joblib')
joblib.dump(tfidf_matrix, 'models/tfidf_model.joblib')

# ---- Neural Embeddings ----
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(corpus, show_progress_bar=True)
joblib.dump(embeddings, 'models/neural_embeddings.pkl')

print("TF-IDF and Neural models saved to 'models/' folder!")
