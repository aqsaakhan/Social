import sys
import os
import json
import logging
from datetime import datetime

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.models import get_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

processed_messages = set()

def process_data(ch, method, properties, body):
    try:
        data = json.loads(body)
        message_id = data.get('id')
        
        if message_id in processed_messages:
            logger.info(f"Skipping already processed message: {message_id}")
            return
        
        processed_messages.add(message_id)
        
        content = data.get('content', '')
        
        logger.info(f"Processing post: {content}")
        
        # Process the data
        word_count = len(content.split())
        char_count = len(content)
        
        logger.info(f"Word count: {word_count}, Character count: {char_count}")
        
        # Store results in the database
        conn = get_db_connection()
        c = conn.cursor()
        
        # Insert the post
        c.execute("INSERT INTO posts (content, timestamp) VALUES (?, ?)",
                  (content, datetime.now().isoformat()))
        post_id = c.lastrowid
        
        logger.info(f"Inserted post with ID: {post_id}")
        
        # Insert analytics associated with the post
        c.execute("INSERT INTO analytics (post_id, type, value, timestamp) VALUES (?, ?, ?, ?)",
                  (post_id, 'Number of Words', str(word_count), datetime.now().isoformat()))
        c.execute("INSERT INTO analytics (post_id, type, value, timestamp) VALUES (?, ?, ?, ?)",
                  (post_id, 'Number of Characters', str(char_count), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Successfully processed and stored analytics for post ID: {post_id}")
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")

# Run this in a separate process
if __name__ == "__main__":
    from message_queue import setup_queue, receive_message
    
    logger.info("Starting data processor...")
    channel = setup_queue()
    logger.info("Queue set up, waiting for messages...")
    receive_message(channel, process_data)