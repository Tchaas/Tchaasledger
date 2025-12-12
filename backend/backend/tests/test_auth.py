"""
Tests for authentication API endpoints.

Tests cover user registration, login, token management, and password operations.
"""
import pytest
from app import db
from app.models import User, Organization


class TestUserRegistration:
    """Tests for user registration endpoint."""

    def test_register_new_user(self, client):
        """Test successful user registration."""
        response = client.post('/api/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'name': 'Test User'
        })

        assert response.status_code == 201
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == 'newuser@example.com'
        assert data['user']['name'] == 'Test User'

    def test_register_with_organization(self, client, test_org):
        """Test registration with organization ID."""
        response = client.post('/api/auth/register', json={
            'email': 'orguser@example.com',
            'password': 'SecurePass123',
            'name': 'Org User',
            'organization_id': test_org.id
        })

        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['organization_id'] == test_org.id

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with existing email."""
        response = client.post('/api/auth/register', json={
            'email': test_user.email,
            'password': 'SecurePass123',
            'name': 'Duplicate User'
        })

        assert response.status_code == 409
        assert 'already registered' in response.get_json()['error'].lower()

    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post('/api/auth/register', json={
            'email': 'not-an-email',
            'password': 'SecurePass123',
            'name': 'Test User'
        })

        assert response.status_code == 400
        assert 'email' in response.get_json()['error'].lower()

    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        weak_passwords = [
            'short',  # Too short
            'alllowercase123',  # No uppercase
            'ALLUPPERCASE123',  # No lowercase
            'NoNumbers',  # No numbers
        ]

        for password in weak_passwords:
            response = client.post('/api/auth/register', json={
                'email': f'test{password}@example.com',
                'password': password,
                'name': 'Test User'
            })

            assert response.status_code == 400
            assert 'password' in response.get_json()['error'].lower()

    def test_register_missing_fields(self, client):
        """Test registration with missing required fields."""
        # Missing email
        response = client.post('/api/auth/register', json={
            'password': 'SecurePass123',
            'name': 'Test User'
        })
        assert response.status_code == 400

        # Missing password
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'name': 'Test User'
        })
        assert response.status_code == 400

        # Missing name
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'SecurePass123'
        })
        assert response.status_code == 400


class TestUserLogin:
    """Tests for user login endpoint."""

    def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post('/api/auth/login', json={
            'email': test_user.email,
            'password': 'TestPass123'
        })

        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['email'] == test_user.email

    def test_login_wrong_password(self, client, test_user):
        """Test login with incorrect password."""
        response = client.post('/api/auth/login', json={
            'email': test_user.email,
            'password': 'WrongPassword123'
        })

        assert response.status_code == 401
        assert 'invalid' in response.get_json()['error'].lower()

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email."""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'SomePass123'
        })

        assert response.status_code == 401
        assert 'invalid' in response.get_json()['error'].lower()

    def test_login_missing_credentials(self, client):
        """Test login with missing fields."""
        # Missing password
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com'
        })
        assert response.status_code == 400

        # Missing email
        response = client.post('/api/auth/login', json={
            'password': 'TestPass123'
        })
        assert response.status_code == 400

    def test_login_case_insensitive_email(self, client, test_user):
        """Test login with different email case."""
        response = client.post('/api/auth/login', json={
            'email': test_user.email.upper(),
            'password': 'TestPass123'
        })

        assert response.status_code == 200


class TestTokenRefresh:
    """Tests for token refresh endpoint."""

    def test_refresh_token(self, client, auth_tokens):
        """Test refreshing access token."""
        refresh_token = auth_tokens['refresh_token']

        response = client.post(
            '/api/auth/refresh',
            headers={'Authorization': f'Bearer {refresh_token}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data

    def test_refresh_with_access_token_fails(self, client, auth_tokens):
        """Test that access token cannot be used for refresh."""
        access_token = auth_tokens['access_token']

        response = client.post(
            '/api/auth/refresh',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code in [401, 422]

    def test_refresh_with_invalid_token(self, client):
        """Test refresh with invalid token."""
        response = client.post(
            '/api/auth/refresh',
            headers={'Authorization': 'Bearer invalid-token'}
        )

        assert response.status_code in [401, 422]


class TestGetCurrentUser:
    """Tests for getting current user profile."""

    def test_get_me_authenticated(self, client, auth_tokens, test_user):
        """Test getting current user profile."""
        response = client.get(
            '/api/auth/me',
            headers={'Authorization': f"Bearer {auth_tokens['access_token']}"}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['email'] == test_user.email
        assert data['user']['name'] == test_user.name

    def test_get_me_unauthenticated(self, client):
        """Test getting profile without authentication."""
        response = client.get('/api/auth/me')

        assert response.status_code in [401, 422]

    def test_get_me_invalid_token(self, client):
        """Test getting profile with invalid token."""
        response = client.get(
            '/api/auth/me',
            headers={'Authorization': 'Bearer invalid-token'}
        )

        assert response.status_code in [401, 422]


class TestUpdateProfile:
    """Tests for updating user profile."""

    def test_update_name(self, client, auth_tokens, test_user):
        """Test updating user name."""
        response = client.put(
            '/api/auth/me',
            headers={'Authorization': f"Bearer {auth_tokens['access_token']}"},
            json={'name': 'Updated Name'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['name'] == 'Updated Name'

        # Verify in database
        db.session.refresh(test_user)
        assert test_user.name == 'Updated Name'

    def test_update_email(self, client, auth_tokens, test_user):
        """Test updating user email."""
        response = client.put(
            '/api/auth/me',
            headers={'Authorization': f"Bearer {auth_tokens['access_token']}"},
            json={'email': 'newemail@example.com'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['email'] == 'newemail@example.com'

    def test_update_email_already_taken(self, client, auth_tokens):
        """Test updating to an email that's already in use."""
        # Create another user
        other_user = User(
            email='other@example.com',
            name='Other User',
            password_hash='hashed'
        )
        db.session.add(other_user)
        db.session.commit()

        response = client.put(
            '/api/auth/me',
            headers={'Authorization': f"Bearer {auth_tokens['access_token']}"},
            json={'email': 'other@example.com'}
        )

        assert response.status_code == 409

    def test_update_invalid_email(self, client, auth_tokens):
        """Test updating to invalid email format."""
        response = client.put(
            '/api/auth/me',
            headers={'Authorization': f"Bearer {auth_tokens['access_token']}"},
            json={'email': 'not-an-email'}
        )

        assert response.status_code == 400


class TestChangePassword:
    """Tests for changing password."""

    def test_change_password_success(self, client, auth_tokens, test_user):
        """Test successful password change."""
        response = client.post(
            '/api/auth/change-password',
            headers={'Authorization': f"Bearer {auth_tokens['access_token']}"},
            json={
                'current_password': 'TestPass123',
                'new_password': 'NewSecurePass123'
            }
        )

        assert response.status_code == 200

        # Verify new password works
        login_response = client.post('/api/auth/login', json={
            'email': test_user.email,
            'password': 'NewSecurePass123'
        })
        assert login_response.status_code == 200

    def test_change_password_wrong_current(self, client, auth_tokens):
        """Test changing password with wrong current password."""
        response = client.post(
            '/api/auth/change-password',
            headers={'Authorization': f"Bearer {auth_tokens['access_token']}"},
            json={
                'current_password': 'WrongPass123',
                'new_password': 'NewSecurePass123'
            }
        )

        assert response.status_code == 401

    def test_change_password_weak_new(self, client, auth_tokens):
        """Test changing to a weak password."""
        response = client.post(
            '/api/auth/change-password',
            headers={'Authorization': f"Bearer {auth_tokens['access_token']}"},
            json={
                'current_password': 'TestPass123',
                'new_password': 'weak'
            }
        )

        assert response.status_code == 400


class TestLogout:
    """Tests for logout endpoint."""

    def test_logout_success(self, client, auth_tokens):
        """Test logout with valid token."""
        response = client.post(
            '/api/auth/logout',
            headers={'Authorization': f"Bearer {auth_tokens['access_token']}"}
        )

        assert response.status_code == 200

    def test_logout_unauthenticated(self, client):
        """Test logout without authentication."""
        response = client.post('/api/auth/logout')

        assert response.status_code in [401, 422]
