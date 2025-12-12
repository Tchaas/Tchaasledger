"""
Authentication utility functions.

Provides password hashing, token generation, and validation helpers.
"""
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app.auth import bcrypt


def hash_password(password):
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(password_hash, password):
    """
    Verify a password against its hash.

    Args:
        password_hash: Stored password hash
        password: Plain text password to verify

    Returns:
        Boolean indicating if password matches
    """
    return bcrypt.check_password_hash(password_hash, password)


def generate_tokens(user_id, organization_id=None):
    """
    Generate JWT access and refresh tokens for a user.

    Args:
        user_id: User's ID
        organization_id: Optional organization ID to include in token

    Returns:
        Tuple of (access_token, refresh_token)
    """
    # Create identity payload
    identity = {
        'user_id': user_id,
        'organization_id': organization_id
    }

    # Generate tokens with expiration times
    access_token = create_access_token(
        identity=identity,
        expires_delta=timedelta(hours=1)
    )

    refresh_token = create_refresh_token(
        identity=identity,
        expires_delta=timedelta(days=30)
    )

    return access_token, refresh_token


def validate_email(email):
    """
    Basic email validation.

    Args:
        email: Email address to validate

    Returns:
        Boolean indicating if email format is valid
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password):
    """
    Validate password meets security requirements.

    Requirements:
    - At least 8 characters
    - Contains uppercase and lowercase letters
    - Contains at least one number

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"

    return True, None
