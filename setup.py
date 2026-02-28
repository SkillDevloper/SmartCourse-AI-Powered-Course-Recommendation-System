import pandas as pd
import numpy as np
import re
import sqlite3
from utils.preprocessing import clean_text

def generate_sample_data():
    """Generate a sample dataset with 8500+ course entries"""
    np.random.seed(42)
    
    departments = [
        'Computer Science', 'Data Science', 'Business', 'Mathematics', 
        'Engineering', 'Biology', 'Chemistry', 'Physics', 'Psychology',
        'Economics', 'History', 'Literature', 'Art', 'Music'
    ]
    
    universities = [
        'Stanford University', 'MIT', 'Harvard University', 'UC Berkeley',
        'Carnegie Mellon', 'University of Michigan', 'Georgia Tech',
        'University of Washington', 'Cornell University', 'Princeton University'
    ]
    
    # Course templates for different departments
    course_templates = {
        'Computer Science': [
            'Introduction to {topic}', 'Advanced {topic}', '{topic} Fundamentals',
            'Applied {topic}', '{topic} for {application}', 'Modern {topic}',
            '{topic} Principles', '{topic} and {related}'
        ],
        'Data Science': [
            'Data {topic}', '{topic} Analytics', 'Statistical {topic}',
            'Machine Learning for {topic}', '{topic} Visualization',
            'Big Data {topic}', '{topic} Mining'
        ],
        'Business': [
            'Business {topic}', 'Strategic {topic}', '{topic} Management',
            'Entrepreneurial {topic}', 'Corporate {topic}', '{topic} Strategy'
        ]
    }
    
    topics = {
        'Computer Science': ['Python', 'Java', 'C++', 'Algorithms', 'Data Structures', 
                           'Web Development', 'Mobile Apps', 'Database Systems',
                           'Operating Systems', 'Computer Networks', 'AI', 
                           'Machine Learning', 'Computer Vision', 'NLP'],
        'Data Science': ['Analysis', 'Science', 'Engineering', 'Visualization',
                        'Mining', 'Warehousing', 'Processing', 'Modeling'],
        'Business': ['Administration', 'Finance', 'Marketing', 'Analytics',
                    'Intelligence', 'Development', 'Operations']
    }
    
    courses = []
    course_id = 1
    
    for dept in departments:
        base_templates = course_templates.get(dept, course_templates['Computer Science'])
        dept_topics = topics.get(dept, topics['Computer Science'])
        
        for uni in universities:
            for _ in range(60):  # Courses per university-department combination
                template = np.random.choice(base_templates)
                topic1 = np.random.choice(dept_topics)
                topic2 = np.random.choice(dept_topics)
                
                # Fill template
                course_name = template.format(topic=topic1, application=topic2, related=topic2)
                
                # Generate description
                descriptions = [
                    f"This course covers fundamental concepts and applications of {topic1} in {dept.lower()}.",
                    f"Learn {topic1} through hands-on projects and real-world applications in {dept.lower()}.",
                    f"Comprehensive study of {topic1} with focus on practical implementation and theoretical foundations.",
                    f"Master {topic1} techniques and methodologies used in modern {dept.lower()} applications.",
                    f"In-depth exploration of {topic1} principles and their applications in various domains."
                ]
                
                description = np.random.choice(descriptions)
                
                # Add some variation
                if np.random.random() > 0.7:
                    description += f" Special focus on {topic2} applications."
                
                course = {
                    'course_id': course_id,
                    'course_name': course_name,
                    'university': uni,
                    'department': dept,
                    'difficulty': np.random.choice(['Beginner', 'Intermediate', 'Advanced']),
                    'rating': round(np.random.uniform(3.5, 5.0), 1),
                    'description': description,
                    'duration_weeks': np.random.randint(4, 16),
                    'price': round(np.random.uniform(0, 200), 2)
                }
                
                courses.append(course)
                course_id += 1
    
    return pd.DataFrame(courses)

def create_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT NOT NULL,
            model_type TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            department TEXT NOT NULL,
            description TEXT NOT NULL,
            model_type TEXT NOT NULL,
            query_text TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create default user
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, username, password) 
        VALUES (1, 'demo_user', 'demo123')
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Generating sample course data...")
    df = generate_sample_data()
    df.to_csv('data/raw_courses.csv', index=False)
    
    print("Cleaning data...")
    df['cleaned_description'] = df['description'].apply(clean_text)
    df.to_csv('data/cleaned_courses.csv', index=False)
    
    print("Creating database...")
    create_database()
    
    print(f"Generated {len(df)} courses")
    print("Setup completed successfully!")