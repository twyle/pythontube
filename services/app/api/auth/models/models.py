"""This module declares the application auth models."""
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin

from ...extensions.extensions import db


class User(UserMixin, db.Model):
    """This class represents a user."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True)
    email = db.Column(db.String(250), unique=True)
    picture = db.Column(db.String(250), unique=True)


class OAuth(OAuthConsumerMixin, db.Model):
    """This class enables atomatic login."""

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
