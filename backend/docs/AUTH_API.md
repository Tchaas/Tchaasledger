# Authentication API Documentation

Complete guide to the Tchaas Ledger authentication system.

## Overview

The authentication system uses **JWT (JSON Web Tokens)** for stateless authentication with the following features:

- **Password Hashing**: Bcrypt for secure password storage
- **Token-based Auth**: JWT access and refresh tokens
- **Validation**: Email format and password strength requirements
- **Security**: Protected routes with decorators
- **Organization Support**: Multi-tenant organization association

## Architecture

```
backend/app/
├── auth/
│   ├── __init__.py          # Auth initialization
│   ├── utils.py             # Password hashing, token generation
│   └── decorators.py        # @login_required, @organization_required
├── routes/
│   └── auth.py              # Authentication endpoints
└── models/
    └── __init__.py          # User model with auth methods
```

## API Endpoints

Base URL: `/api/auth`

### 1. Register New User

**POST** `/api/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe",
  "organization_id": 1  // Optional
}
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

**Response** (201 Created):
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "organization_id": 1,
    "created_at": "2024-01-01T00:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors:**
- `400`: Invalid email format or weak password
- `409`: Email already registered
- `404`: Organization not found (if organization_id provided)

---

### 2. Login

**POST** `/api/auth/login`

Authenticate with email and password.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response** (200 OK):
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "organization_id": 1,
    "created_at": "2024-01-01T00:00:00"
  },
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors:**
- `400`: Missing email or password
- `401`: Invalid credentials

---

### 3. Refresh Access Token

**POST** `/api/auth/refresh`

Get a new access token using refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response** (200 OK):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Errors:**
- `401`: Invalid or expired refresh token

---

### 4. Get Current User

**GET** `/api/auth/me`

Get the authenticated user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "organization_id": 1,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Errors:**
- `401`: Not authenticated
- `404`: User not found

---

### 5. Update Profile

**PUT** `/api/auth/me`

Update the authenticated user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "email": "newemail@example.com"
}
```

**Response** (200 OK):
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "email": "newemail@example.com",
    "name": "Updated Name",
    "organization_id": 1,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

**Errors:**
- `400`: Invalid email format
- `401`: Not authenticated
- `409`: Email already in use

---

### 6. Change Password

**POST** `/api/auth/change-password`

Change the user's password.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "OldPass123",
  "new_password": "NewSecurePass123"
}
```

**Response** (200 OK):
```json
{
  "message": "Password changed successfully"
}
```

**Errors:**
- `400`: Weak new password
- `401`: Incorrect current password

---

### 7. Logout

**POST** `/api/auth/logout`

Logout (client should discard tokens).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response** (200 OK):
```json
{
  "message": "Logout successful"
}
```

---

## Token Management

### Token Expiration

- **Access Token**: 1 hour
- **Refresh Token**: 30 days

### Token Format

Tokens contain the following payload:
```json
{
  "user_id": 1,
  "organization_id": 1
}
```

### Using Tokens

Include the access token in the Authorization header:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## Protected Routes

Use decorators to protect routes:

### @login_required

Requires valid JWT token.

```python
from app.auth.decorators import login_required

@app.route('/protected')
@login_required
def protected_route():
    return {'message': 'authenticated'}
```

### @organization_required

Requires user belongs to an organization.

```python
from app.auth.decorators import organization_required

@app.route('/org-only')
@organization_required
def org_route():
    return {'message': 'user has organization'}
```

### Getting Current User

```python
from app.auth.decorators import get_current_user, get_current_organization

@app.route('/profile')
@login_required
def profile():
    user = get_current_user()
    org = get_current_organization()
    return {
        'user': user.to_dict(),
        'organization': org.to_dict() if org else None
    }
```

---

## User Model Methods

The User model includes convenience methods:

```python
from app.models import User

# Create user with password
user = User(email='user@example.com', name='Test User')
user.set_password('SecurePass123')

# Verify password
if user.check_password('SecurePass123'):
    print('Password correct!')
```

---

## Security Best Practices

### Password Storage
- Passwords are hashed using bcrypt
- Never store plain text passwords
- Salt is automatically generated per password

### Token Security
- Store tokens securely on client (httpOnly cookies recommended)
- Don't expose tokens in URLs
- Implement token rotation
- Use HTTPS in production

### Password Requirements
- Minimum 8 characters
- Mix of uppercase, lowercase, and numbers
- Consider adding special characters requirement

---

## Testing

Run authentication tests:

```bash
cd backend
pytest backend/tests/test_auth.py -v
```

### Test Coverage

- User registration (valid/invalid)
- Login (success/failure)
- Token refresh
- Profile management
- Password changes
- Logout

---

## Example Usage

### Frontend Integration

```javascript
// Register
const register = async (email, password, name) => {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, name })
  });
  const data = await response.json();

  // Store tokens
  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);

  return data.user;
};

// Login
const login = async (email, password) => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();

  localStorage.setItem('access_token', data.access_token);
  localStorage.setItem('refresh_token', data.refresh_token);

  return data.user;
};

// Make authenticated request
const getProfile = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch('/api/auth/me', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
};

// Refresh token
const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  const response = await fetch('/api/auth/refresh', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${refreshToken}` }
  });
  const data = await response.json();

  localStorage.setItem('access_token', data.access_token);
  return data.access_token;
};
```

---

## Configuration

JWT settings in [config.py](/backend/config.py):

```python
# JWT Authentication
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_TOKEN_LOCATION = ['headers']
JWT_HEADER_NAME = 'Authorization'
JWT_HEADER_TYPE = 'Bearer'
```

### Environment Variables

```bash
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here  # Optional, defaults to SECRET_KEY
```

---

## Troubleshooting

### Common Issues

**401 Unauthorized**
- Check token is included in Authorization header
- Verify token hasn't expired
- Ensure token format: `Bearer <token>`

**422 Unprocessable Entity**
- Token format is invalid
- Token signature verification failed
- Check JWT_SECRET_KEY matches

**Password validation fails**
- Verify password meets all requirements
- Check for minimum length, uppercase, lowercase, numbers

---

## Next Steps

1. **Implement token blacklisting** - For proper logout functionality
2. **Add email verification** - Confirm email addresses
3. **Password reset flow** - Forgot password functionality
4. **Role-based access control** - Add user roles and permissions
5. **Two-factor authentication** - Additional security layer
6. **OAuth integration** - Social login (Google, GitHub, etc.)

---

## Files Reference

- [auth/__init__.py](/backend/app/auth/__init__.py) - Auth initialization
- [auth/utils.py](/backend/app/auth/utils.py) - Password hashing, token utils
- [auth/decorators.py](/backend/app/auth/decorators.py) - Route protection
- [routes/auth.py](/backend/app/routes/auth.py) - API endpoints
- [models/__init__.py](/backend/app/models/__init__.py) - User model
- [tests/test_auth.py](/backend/backend/tests/test_auth.py) - Test suite
