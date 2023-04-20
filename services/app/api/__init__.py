"""This module creates the Flask app object."""
import sys

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for
from flask_dance.contrib.google import google
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
from sqlalchemy.exc import OperationalError

from .auth.models.models import User
from .exceptions.exceptions import DatabaseNotConnectedException
from .extensions.extensions import db, login_manager
from .helpers.helpers import (
    check_configuration,
    register_blueprints,
    register_extensions,
    set_configuration,
)
from .utils.http_status_codes import HTTP_200_OK

load_dotenv()


def create_app() -> Flask:
    """Create the Flask app instance."""
    app = Flask(__name__)

    set_configuration(app)
    try:
        check_configuration()
    except DatabaseNotConnectedException as e:
        print(str(e))
        sys.exit(1)

    register_extensions(app)
    register_blueprints(app)

    @app.route("/login_page")
    def login_page():
        return render_template("auth/landing_page.html"), HTTP_200_OK

    @app.route("/login")
    def login():
        try:
            if not google.authorized:
                return redirect(url_for("google.login"))
            resp = google.get("/oauth2/v1/userinfo")
            if resp.ok:
                return redirect(url_for("home.home_page"))
            return redirect(url_for("login_page"))
        except (TokenExpiredError, InvalidGrantError):
            return redirect(url_for("google.login"))

    @login_manager.user_loader
    def load_user(user_id):
        user = None
        try:
            user = User.query.get(int(user_id))
        except OperationalError:
            print("Unable to connect to database!")
            sys.exit(1)
        return user

    @app.route("/health")
    def home():
        return "Hello world!", HTTP_200_OK

    app.shell_context_processor({"app": app})

    return app
