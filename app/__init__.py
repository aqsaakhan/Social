from flask import Flask
from flask_socketio import SocketIO
import logging

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    from .routes import main
    app.register_blueprint(main)

    socketio.init_app(app, async_mode='threading')  # Use threading mode for long-polling

    return app