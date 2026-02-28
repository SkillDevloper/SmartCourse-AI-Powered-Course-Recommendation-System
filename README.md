# SmartCourse – AI Powered Course Recommendation System

**Domain:** Machine Learning / Natural Language Processing (NLP)

SmartCourse is an intelligent course recommendation engine built with dual algorithms. It uses both a classical TF‑IDF vectorizer for keyword matching and a neural sentence-transformers model for semantic understanding. Users submit natural language preferences and receive personalized course lists drawn from a large corpus of (>8,500) course descriptions. The system guarantees different recommendations for identical queries by comparing the two models side-by-side.

---

## ✅ Key Features

- Dual recommendation engines (TF‑IDF and neural embeddings)
- Full-stack Flask web interface with multi-page layout
  - Home, recommendation page, dashboard, about
- Text input with model chooser and 10-item results
  - Display course title, university, department, description
  - Relevance score (0-100%) with progress bar
  - Save favourites and revisit by session
- Dashboard showing search history and saved courses
- Side-by-side comparison of model outputs for the same query
- REST API for programmatic access (`/api/recommend`, `/api/history`, etc.)

---
## Screenshots
![Home](https://github.com/SkillDevloper/SmartCourse-AI-Powered-Course-Recommendation-System/blob/main/Screenshots/Home%20Page.png)
![About](https://github.com/SkillDevloper/SmartCourse-AI-Powered-Course-Recommendation-System/blob/main/Screenshots/About%20Page.png)
![Dashboard](https://github.com/SkillDevloper/SmartCourse-AI-Powered-Course-Recommendation-System/blob/main/Screenshots/User%20Dashboard%20Page.png)
![Recommendation](https://github.com/SkillDevloper/SmartCourse-AI-Powered-Course-Recommendation-System/blob/main/Screenshots/Recommendation%20Page.png)
---

## 🛠 Installation & Setup

1. **Ensure Python 3.10+ is installed**
   ```bash
   python --version
   ```

2. **Clone the repository and change directory**
   ```bash
   git clone https://github.com/SkillDevloper/SmartCourse-AI-Powered-Course-Recommendation-System.git
   cd SmartCourse
   ```

3. **Create a Python virtual environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Download the spaCy English model**
   ```bash
   python -m spacy download en_core_web_sm-3.7.1
   ```

6. **Generate and clean dataset, build database**
   ```bash
   python setup.py
   ```
   This creates `data/raw_courses.csv` and `data/cleaned_courses.csv` and initializes `database.db`.

7. **Train both recommendation models**
   ```bash
   python train_models.py
   ```

8. **Start the Flask application**
   ```bash
   python app.py
   ```
   Open `http://localhost:5000` in your browser.

---

## 📁 Project Structure

```
SmartCourse/
├── app.py                      # Main Flask application
├── setup.py                    # Data generation and setup
├── train_models.py             # Train TF-IDF and neural models
├── requirements.txt            # Python dependencies
├── data/
│   ├── raw_courses.csv         # Generated raw course data
│   └── cleaned_courses.csv     # Cleaned and preprocessed data
├── models/                     # Trained model files
│   ├── tfidf_model.joblib
│   ├── tfidf_vectorizer.joblib
│   └── neural_embeddings.pkl
├── utils/
│   ├── preprocessing.py        # Text cleaning and preprocessing
│   ├── recommend_tfidf.py      # TF-IDF recommendation engine
│   └── recommend_neural.py     # Neural embedding recommendation engine
├── templates/                  # HTML templates
│   ├── home.html
│   ├── recommend.html
│   ├── dashboard.html
│   └── about.html
├── static/                     # CSS, JavaScript, images
│   ├── css/
│   ├── js/
│   └── images/
├── database.db                 # SQLite database (auto-created)
```

---

## 📡 API Endpoints

| Method | Path                 | Description                        |
|--------|----------------------|------------------------------------|
| POST   | `/api/recommend`     | Returns top-10 courses for a query |
| GET    | `/api/history`       | Search history (latest 50 entries) |
| POST   | `/api/save`          | Save a recommended course          |
| GET    | `/api/saved-courses` | Retrieve saved courses             |

**Request Example:**
```json
{
  "query": "I want to learn Python for data science",
  "model": "neural"
}
```

**Response Example:**
```json
{
  "success": true,
  "recommendations": [
    {
      "course_name": "Advanced Python for Data Science",
      "university": "MIT",
      "department": "Computer Science",
      "difficulty": "Intermediate",
      "rating": 4.8,
      "description": "...",
      "score": 0.85,
      "score_percentage": 85.0
    }
  ]
}
```

---

## 🧠 Technical Details

### TF-IDF Model
- **Vectorizer:** scikit-learn `TfidfVectorizer`
- **N-gram range:** (1, 2) — unigrams and bigrams
- **Matching:** Cosine similarity over cleaned course descriptions
- **Use case:** Keyword-focused recommendations

### Neural Model
- **Model:** Sentence-BERT (`all-MiniLM-L6-v2`)
- **Embedding dimension:** 384
- **Matching:** Cosine similarity in embedding space
- **Use case:** Semantic and conceptual recommendations

### Data Processing Pipeline
1. Remove HTML tags and special characters
2. Convert to lowercase
3. Tokenize using spaCy
4. Remove stopwords and punctuation
5. Lemmatization
6. Handle missing values

### Evaluation Metrics (Future Enhancement)
- Precision@K
- Recall@K
- Hit-rate

---

## 💡 Sample Queries to Test

```
"I want to learn Python for data science"
"Machine learning and artificial intelligence courses"
"Business analytics and data visualization"
"Web development with JavaScript"
"Computer science fundamentals"
```

---

## 🚀 Quick Start

```bash
# 1. Set up environment
python -m venv .venv
.\.venv\Scripts\activate

# 2. Install and configure
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm-3.7.1

# 3. Generate data and train models
python setup.py
python train_models.py

# 4. Run the application
python app.py

# 5. Open browser
# Navigate to http://localhost:5000
```

---

## 📜 License

MIT License

---

## 👨‍💻 Contributors

Built as a course recommendation system project demonstrating full-stack ML development.

---

Happy learning and recommending!
