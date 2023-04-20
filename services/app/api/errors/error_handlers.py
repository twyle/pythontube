"""This module declares all the error handlesr for the app."""
from flask import Blueprint, render_template

from ..utils.http_status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """Handle all 404 page not found errors."""
    print(error)
    return render_template("errors/404.html"), HTTP_404_NOT_FOUND


@errors.app_errorhandler(405)
def error_405(error):
    """Handle all 405 method not allowed errors."""
    print(error)
    return render_template("errors/405.html"), HTTP_405_METHOD_NOT_ALLOWED


@errors.app_errorhandler(500)
def error_500(error):
    """Handle all 500 server down errors."""
    print(error)
    return render_template("errors/500.html"), HTTP_500_INTERNAL_SERVER_ERROR
