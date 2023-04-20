"""This module declares the extensions used by the application."""
import os

from dotenv import load_dotenv
from flask_cors import CORS
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from youtube import YouTube

load_dotenv()

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
login_manager = LoginManager()

client_secrets_file = os.environ["CLIENT_SECRETS_FILE"]
token_path = os.environ.get("TOKEN_PATH", "")
youtube = YouTube()
youtube.authenticate_from_client_secrets_file(client_secrets_file)
