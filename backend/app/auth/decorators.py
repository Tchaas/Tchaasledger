"""
Authentication decorators for protecting routes.

Provides decorators to require authentication and organization membership.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User, Organization
from app import db


def login_required(fn):
    """
    Decorator to require valid JWT token for route access.

    Usage:
        @app.route('/protected')
        @login_required
        def protected_route():
            return {'message': 'authenticated'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': 'Authentication required',
                'message': str(e)
            }), 401

    return wrapper


def organization_required(fn):
    """
    Decorator to require user belongs to an organization.

    Usage:
        @app.route('/org-only')
        @organization_required
        def org_route():
            return {'message': 'user has organization'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            identity = get_jwt_identity()

            if not identity.get('organization_id'):
                return jsonify({
                    'error': 'Organization required',
                    'message': 'User must belong to an organization'
                }), 403

            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': 'Authentication required',
                'message': str(e)
            }), 401

    return wrapper


def get_current_user():
    """
    Get the current authenticated user from JWT token.

    Returns:
        User object or None if not authenticated
    """
    try:
        verify_jwt_in_request()
        identity = get_jwt_identity()
        user_id = identity.get('user_id')

        if user_id:
            return User.query.get(user_id)

        return None
    except Exception:
        return None


def get_current_organization():
    """
    Get the current user's organization from JWT token.

    Returns:
        Organization object or None if not authenticated/no org
    """
    try:
        verify_jwt_in_request()
        identity = get_jwt_identity()
        org_id = identity.get('organization_id')

        if org_id:
            return Organization.query.get(org_id)

        return None
    except Exception:
        return None


def admin_required(fn):
    """
    Decorator to require admin privileges.
    (For future use when role-based access control is implemented)

    Usage:
        @app.route('/admin-only')
        @admin_required
        def admin_route():
            return {'message': 'admin access'}
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user = get_current_user()

            if not user:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Invalid or expired token'
                }), 401

            # TODO: Implement role checking when roles are added to User model
            # For now, just check if user exists
            return fn(*args, **kwargs)

        except Exception as e:
            return jsonify({
                'error': 'Authentication required',
                'message': str(e)
            }), 401

    return wrapper
