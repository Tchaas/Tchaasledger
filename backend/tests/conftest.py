"""
Pytest configuration and fixtures for tests.
"""
import os
import pytest
from app import create_app
from app.models import db


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    # Set test environment variables
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['TESTING'] = 'True'
    os.environ['DATABASE_URL'] = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/tchaas_ledger_test'
    )
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['ENABLE_GCP_MONITORING'] = 'false'

    # Create app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

    return app


@pytest.fixture(scope='session')
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope='session')
def _db(app):
    """Create database for testing."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def session(_db):
    """Create a new database session for a test."""
    connection = _db.engine.connect()
    transaction = connection.begin()

    # Bind session to connection
    session = _db.create_scoped_session(
        options={"bind": connection, "binds": {}}
    )
    _db.session = session

    yield session

    # Rollback and cleanup
    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def test_org(session):
    """Create a test organization."""
    from app.models import Organization

    org = Organization(
        name='Test Organization',
        ein='12-3456789',
        address='123 Test St',
        city='Test City',
        state='CA',
        zip_code='12345'
    )
    session.add(org)
    session.commit()
    return org


@pytest.fixture
def test_user(session, test_org):
    """Create a test user."""
    from app.models import User
    from app.auth.utils import hash_password

    user = User(
        email='test@example.com',
        name='Test User',
        password_hash=hash_password('TestPass123'),
        organization_id=test_org.id
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def auth_tokens(client, test_user):
    """Generate authentication tokens for test user."""
    response = client.post('/api/auth/login', json={
        'email': test_user.email,
        'password': 'TestPass123'
    })

    data = response.get_json()
    return {
        'access_token': data['access_token'],
        'refresh_token': data['refresh_token']
    }
