import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('74453d326893031f1499b21b6d0b5cce683fe3367cbd922a') or 'you-will-never-guess'
    DEBUG = os.environ.get('FLASK_DEBUG') or False