"""
Authentication routes for JWT-based login/registration
Enhanced Security for Phase 3
"""
from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    unset_jwt_cookies,
)
from werkzeug.exceptions import BadRequest, Unauthorized

from extensions import db, limiter
from models import User
from validators import validate_password_strength, sanitize_string

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def role_required(*roles):
    """Decorator to require specific roles"""
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims['role'] not in roles:
                raise Unauthorized("Insufficient permissions")
            return fn(*args, **kwargs)
        return decorator
    return wrapper


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("3 per hour")  # Limit registration attempts
def register():
    """Register a new user with password strength validation"""
    data = request.get_json()

    if not data:
        raise BadRequest("No data provided")

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data or not data[field].strip():
            raise BadRequest(f"Missing required field: {field}")

    username = sanitize_string(data['username'])
    email = sanitize_string(data['email']).lower()
    password = data['password']
    role = data.get('role', 'user')

    # Validate username
    if len(username) < 3:
        raise BadRequest("Username must be at least 3 characters")
    if len(username) > 80:
        raise BadRequest("Username must be less than 80 characters")

    # Validate email
    if '@' not in email or '.' not in email:
        raise BadRequest("Invalid email format")

    # Validate password strength
    is_valid, errors, score, strength_level = validate_password_strength(password)
    if not is_valid:
        raise BadRequest(f"Password too weak: {'; '.join(errors)}")

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        raise BadRequest("Username already taken")
    if User.query.filter_by(email=email).first():
        raise BadRequest("Email already registered")

    # Create new user
    user = User(
        username=username,
        email=email,
        role=role if role in ['admin', 'user', 'viewer'] else 'user'
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    # Create tokens
    access_token = create_access_token(
        # flask-jwt-extended expects token "sub" to be a string.
        identity=str(user.id),
        additional_claims={'role': user.role, 'username': user.username}
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'username': user.username}
    )

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 201


@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limit login attempts
def login():
    """Login user with account lockout protection"""
    data = request.get_json()

    if not data:
        raise BadRequest("No data provided")

    username = sanitize_string(data.get('username', ''))
    password = data.get('password', '')

    if not username or not password:
        raise BadRequest("Username and password required")

    # Find user
    user = User.query.filter_by(username=username).first()

    if not user:
        # Record failed attempt for non-existent user (prevent enumeration)
        # In production, you might want to skip this to avoid creating dummy accounts
        raise Unauthorized("Invalid username or password")

    # Check if account is locked
    if user.is_locked():
        minutes_left = (user.locked_until - datetime.utcnow()).seconds // 60 + 1
        raise Unauthorized(f"Account locked due to multiple failed attempts. Try again in {minutes_left} minutes.")

    if not user.is_active:
        raise Unauthorized("Account is disabled")

    # Check password
    if not user.check_password(password):
        # Record failed login
        user.record_failed_login()
        
        if user.is_locked():
            raise Unauthorized("Account locked due to multiple failed attempts. Try again in 15 minutes.")
        else:
            attempts_left = 5 - user.failed_login_attempts
            raise Unauthorized(f"Invalid username or password. {attempts_left} attempts remaining.")

    # Successful login - reset failed attempts
    user.update_last_login()

    # Create tokens
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'username': user.username},
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'username': user.username},
        expires_delta=timedelta(days=30)
    )

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token using refresh token"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    
    user = User.query.get(int(current_user_id))
    if not user or not user.is_active:
        raise Unauthorized("User not found or inactive")
    
    access_token = create_access_token(
        identity=str(current_user_id),
        additional_claims={'role': claims['role'], 'username': claims['username']},
        expires_delta=timedelta(hours=1)
    )
    
    return jsonify({
        "access_token": access_token
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user by clearing JWT cookies"""
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user information"""
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        raise Unauthorized("User not found")
    
    return jsonify({
        "user": user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current user profile with password strength validation"""
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))

    if not user:
        raise Unauthorized("User not found")

    data = request.get_json()
    if not data:
        raise BadRequest("No data provided")

    # Updatable fields
    if 'email' in data:
        email = sanitize_string(data['email']).lower()
        if '@' not in email or '.' not in email:
            raise BadRequest("Invalid email format")

        # Check if email is taken by another user
        existing = User.query.filter_by(email=email).first()
        if existing and existing.id != user.id:
            raise BadRequest("Email already in use")
        user.email = email

    if 'password' in data:
        # Validate password strength
        is_valid, errors, score, strength_level = validate_password_strength(data['password'])
        if not is_valid:
            raise BadRequest(f"Password too weak: {'; '.join(errors)}")
        user.set_password(data['password'])

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "user": user.to_dict()
    }), 200


@auth_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_users():
    """Get all users (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)
    users = pagination.items
    
    return jsonify({
        "users": [user.to_dict() for user in users],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page
    }), 200


@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user(user_id):
    """Update user role or status (admin only)"""
    user = User.query.get(user_id)
    if not user:
        raise BadRequest("User not found")
    
    data = request.get_json()
    if not data:
        raise BadRequest("No data provided")
    
    if 'role' in data:
        role = data['role']
        if role not in ['admin', 'user', 'viewer']:
            raise BadRequest("Invalid role")
        user.role = role
    
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        "message": "User updated successfully",
        "user": user.to_dict()
    }), 200


@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    """Delete a user (admin only)"""
    user = User.query.get(user_id)
    if not user:
        raise BadRequest("User not found")
    
    # Prevent self-deletion
    current_user_id = get_jwt_identity()
    if user_id == int(current_user_id):
        raise BadRequest("Cannot delete your own account")
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"}), 200
