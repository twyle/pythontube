"""This module declares methods for the login module."""
import sys

from dotenv import load_dotenv
from flask import Blueprint, redirect, url_for
from flask_dance.consumer import oauth_authorized
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.google import google, make_google_blueprint
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound

from ..extensions.extensions import db
from .models.models import OAuth, User

load_dotenv()


auth = Blueprint("auth", __name__)

google_blueprint = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    """Automatically log in a user."""
    info = google.get("/oauth2/v1/userinfo")
    if info.ok:
        account_info = info.json()
        email = account_info["email"]

        query = User.query.filter_by(email=email)
        try:
            user = query.one()
        except NoResultFound:
            user = User(
                email=email, name=account_info["name"], picture=account_info["picture"]
            )
            db.session.add(user)
            db.session.commit()
        except OperationalError:
            print("Unable to connect to database!")
            sys.exit(1)
        login_user(user)
        return redirect(url_for("home.home_page"))
    return redirect(url_for("login_page"))


@auth.route("/logout")
@login_required
def logout():
    """Logout a logged in user."""
    logout_user()
    return redirect(url_for("login_page"))
