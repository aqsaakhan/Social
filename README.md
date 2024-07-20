# Social Media Analytics Dashboard

A web application for creating and analyzing social media posts in real-time.

## Features

- Create and store social media posts
- Real-time analytics: word count and character count
- Asynchronous processing with RabbitMQ
- RESTful API

## Tech Stack

- Backend: Python 3.7+, Flask
- Frontend: HTML, JavaScript
- Database: SQLite
- Message Queue: RabbitMQ

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up RabbitMQ
4. Run the Flask app: `flask run`
5. Run the data processor: `python data_processor.py`

## Usage

Access the web interface at `http://localhost:5000`