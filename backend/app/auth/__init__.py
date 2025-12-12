"""
Authentication module for Tchaas Ledger.

Provides JWT-based authentication with password hashing and token management.
"""
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()


def init_auth(app):
    """
    Initialize authentication extensions with the Flask app.

    Args:
        app: Flask application instance
    """
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.logger.info("Authentication initialized successfully")
