"""This module delares helper methods for the whole app.

Declares the following config:

set_configuration:
    For setting the apps configuration.
register_blueprints:
    For registering the application blueprints.
register_extensions:
    For registering the application extensions.
"""
import os

from flask import Flask

from ..auth.views import auth, google_blueprint
from ..config.config import Config
from ..errors.error_handlers import errors
from ..exceptions.exceptions import DatabaseNotConnectedException
from ..extensions.extensions import cors, db, login_manager, ma, migrate
from ..utils.utils import check_if_database_exists, create_db_conn_string
from ..home.views import home


def set_configuration(app):
    """Set the application configuration.

    The application configuration will depend on the
    environment i.e Test, Development, Staging or Production.

    Parameters
    ----------
    app: flask.Flask
        A flask app instance

    Returns
    -------
    bool:
        Whether the config was set up successfully.
    """
    config_name = os.environ.get("FLASK_ENV")
    app.config.from_object(Config[config_name])

    return True


def check_configuration():
    """Check if all the configs are set."""
    # Check database connection
    if not check_if_database_exists(create_db_conn_string()):
        raise DatabaseNotConnectedException("The database is not connected!")


def register_extensions(app: Flask):
    """Register the app extensions."""
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login_page"


def register_blueprints(app: Flask) -> bool:
    """Register the application blueprints.

    Parameters
    ----------
    app: flask.Flask
        A flask app instance

    Returns
    -------
    bool:
        Whether all the blueprints were registered.
    """
    app.register_blueprint(home)
    app.register_blueprint(google_blueprint, url_prefix="/login")
    return True
