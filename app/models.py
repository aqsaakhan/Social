import sqlite3
from datetime import datetime
import os

# Determine the base directory
if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    # We're on PythonAnywhere
    BASE_DIR = '/home/ahsankhan97/social_media_analytics'
else:
    # We're running locally
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database file path
DB_PATH = os.path.join(BASE_DIR, 'data', 'analytics.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id INTEGER PRIMARY KEY, content TEXT, timestamp DATETIME)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS analytics
                 (id INTEGER PRIMARY KEY, post_id INTEGER, type TEXT, value TEXT, timestamp DATETIME,
                 FOREIGN KEY (post_id) REFERENCES posts (id))''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_post_with_analytics(content):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Add post
    c.execute("INSERT INTO posts (content, timestamp) VALUES (?, ?)",
              (content, datetime.now().isoformat()))
    post_id = c.lastrowid
    
    # Calculate analytics
    word_count = len(content.split())
    char_count = len(content)
    
    # Add analytics
    c.execute("INSERT INTO analytics (post_id, type, value, timestamp) VALUES (?, ?, ?, ?)",
              (post_id, 'word_count', str(word_count), datetime.now().isoformat()))
    c.execute("INSERT INTO analytics (post_id, type, value, timestamp) VALUES (?, ?, ?, ?)",
              (post_id, 'char_count', str(char_count), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()