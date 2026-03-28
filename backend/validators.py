"""
Input validation and sanitization utilities
Enhanced Security for Phase 3
"""
import re
import html
from functools import wraps
from flask import request, jsonify
from werkzeug.exceptions import BadRequest


# Email validation regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Phone validation (international format)
PHONE_REGEX = re.compile(r'^\+?[\d\s\-\(\)]{10,}$')

# Tax ID validation (Indian GST format)
GST_REGEX = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')

# PAN validation (Indian PAN)
PAN_REGEX = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')

# Bank account validation (Indian format)
BANK_ACCOUNT_REGEX = re.compile(r'^[0-9]{9,18}$')

# IFSC code validation
IFSC_REGEX = re.compile(r'^[A-Z]{4}0[A-Z0-9]{6}$')

# Postal code validation (Indian PIN)
PINCODE_REGEX = re.compile(r'^[1-9][0-9]{5}$')

# Password strength validation
PASSWORD_STRENGTH_REGEX = {
    'min_length': re.compile(r'^.{8,}$'),
    'uppercase': re.compile(r'[A-Z]'),
    'lowercase': re.compile(r'[a-z]'),
    'digit': re.compile(r'[0-9]'),
    'special': re.compile(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;\'`~]')
}


def validate_password_strength(password):
    """
    Validate password strength
    Returns tuple: (is_valid, errors, strength_score)
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    
    Strength Score:
    - 0-40: Weak
    - 41-70: Medium
    - 71-100: Strong
    """
    errors = []
    score = 0
    
    if not password:
        return False, ["Password is required"], 0
    
    # Check minimum length
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")
    else:
        score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
    
    # Check for uppercase
    if PASSWORD_STRENGTH_REGEX['uppercase'].search(password):
        score += 15
    else:
        errors.append("Password must contain at least one uppercase letter")
    
    # Check for lowercase
    if PASSWORD_STRENGTH_REGEX['lowercase'].search(password):
        score += 15
    else:
        errors.append("Password must contain at least one lowercase letter")
    
    # Check for digit
    if PASSWORD_STRENGTH_REGEX['digit'].search(password):
        score += 15
    else:
        errors.append("Password must contain at least one number")
    
    # Check for special character
    if PASSWORD_STRENGTH_REGEX['special'].search(password):
        score += 15
    else:
        errors.append("Password must contain at least one special character (!@#$%^&*...)")
    
    # Check for common passwords
    common_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein', 'welcome', 'monkey', 'dragon']
    if password.lower() in common_passwords:
        errors.append("Password is too common. Please choose a stronger password")
        score = max(0, score - 30)
    
    # Check for sequential characters
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        score = max(0, score - 10)
    
    strength_level = 'weak' if score <= 40 else 'medium' if score <= 70 else 'strong'
    
    return len(errors) == 0, errors, min(100, score), strength_level


def sanitize_string(value, max_length=255):
    """
    Sanitize string input
    - Remove leading/trailing whitespace
    - Remove potentially dangerous characters
    - Limit length
    """
    if value is None:
        return None

    if not isinstance(value, str):
        value = str(value)

    # Strip whitespace
    value = value.strip()

    # Remove null bytes
    value = value.replace('\x00', '')

    # Limit length
    if len(value) > max_length:
        value = value[:max_length]

    return value


def sanitize_html(value):
    """
    Remove potentially dangerous HTML tags and scripts
    Enhanced sanitization for XSS prevention
    """
    if value is None:
        return None

    # First escape all HTML entities
    value = html.escape(value)

    # Remove script tags and content
    value = re.sub(r'<script\b[^>]*>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)

    # Remove other potentially dangerous tags
    dangerous_tags = ['iframe', 'object', 'embed', 'form', 'input', 'button', 'link', 'meta', 'style']
    for tag in dangerous_tags:
        value = re.sub(f'<{tag}\b[^>]*>.*?</{tag}>', '', value, flags=re.IGNORECASE | re.DOTALL)
        value = re.sub(f'<{tag}\b[^>]*/?>', '', value, flags=re.IGNORECASE)

    # Remove javascript: protocol
    value = re.sub(r'javascript:', '', value, flags=re.IGNORECASE)
    
    # Remove on* event handlers
    value = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', value, flags=re.IGNORECASE)

    return value


def sanitize_sql_input(value):
    """
    Sanitize input to prevent SQL injection
    Note: SQLAlchemy ORM provides protection, but this adds extra layer
    """
    if value is None:
        return None
    
    if not isinstance(value, str):
        return value
    
    # Remove common SQL injection patterns
    sql_patterns = [
        r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE)\b)',
        r'(--|#|/\*)',
        r'(\b(OR|AND)\b\s+\d+\s*=\s*\d+)',
    ]
    
    for pattern in sql_patterns:
        value = re.sub(pattern, '', value, flags=re.IGNORECASE)
    
    return value


def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return False
    return bool(PHONE_REGEX.match(phone.strip()))


def validate_gst(gst):
    """Validate GST number format"""
    if not gst:
        return True  # Optional field
    return bool(GST_REGEX.match(gst.strip().upper()))


def validate_pan(pan):
    """Validate PAN number format"""
    if not pan:
        return True  # Optional field
    return bool(PAN_REGEX.match(pan.strip().upper()))


def validate_bank_account(account):
    """Validate bank account number format"""
    if not account:
        return True  # Optional field
    cleaned = account.replace(' ', '').replace('-', '')
    return bool(BANK_ACCOUNT_REGEX.match(cleaned))


def validate_pincode(pincode):
    """Validate Indian PIN code"""
    if not pincode:
        return True  # Optional field
    return bool(PINCODE_REGEX.match(pincode.strip()))


def validate_vendor_data(data):
    """
    Validate vendor data comprehensively
    Returns tuple: (is_valid, errors)
    """
    errors = []
    
    if not data:
        return False, ["No data provided"]
    
    # Required fields
    if not data.get('id'):
        errors.append("Vendor ID is required")
    else:
        data['id'] = sanitize_string(data['id'], max_length=50)
    
    if not data.get('vendor_name'):
        errors.append("Vendor name is required")
    else:
        data['vendor_name'] = sanitize_string(data['vendor_name'], max_length=255)
    
    # Optional fields validation
    if data.get('contact_email'):
        if not validate_email(data['contact_email']):
            errors.append("Invalid email format")
        else:
            data['contact_email'] = sanitize_string(data['contact_email'], max_length=255)
    
    if data.get('contact_phone'):
        if not validate_phone(data['contact_phone']):
            errors.append("Invalid phone number format")
        else:
            data['contact_phone'] = sanitize_string(data['contact_phone'], max_length=20)
    
    if data.get('tax_id'):
        data['tax_id'] = sanitize_string(data['tax_id'], max_length=50).upper()
        if not validate_gst(data['tax_id']):
            errors.append("Invalid GST number format")
    
    if data.get('bank_account'):
        data['bank_account'] = sanitize_string(data['bank_account'], max_length=50)
        if not validate_bank_account(data['bank_account']):
            errors.append("Invalid bank account format")
    
    if data.get('postal_code'):
        data['postal_code'] = sanitize_string(data['postal_code'], max_length=20)
        if not validate_pincode(data['postal_code']):
            errors.append("Invalid PIN code format")
    
    # Sanitize text fields
    for field in ['details', 'address_line1', 'city', 'state', 'country', 'contact_person']:
        if data.get(field):
            data[field] = sanitize_string(data[field], max_length=255 if field != 'details' else 2000)
            if field == 'details':
                data[field] = sanitize_html(data[field])
    
    # Date validation
    if data.get('manufacture_date'):
        try:
            from datetime import datetime
            datetime.strptime(data['manufacture_date'], '%Y-%m-%d')
        except ValueError:
            errors.append("Invalid date format. Use YYYY-MM-DD")
    
    return len(errors) == 0, errors


def require_valid_json(f):
    """Decorator to require valid JSON in request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                "error": "Bad Request",
                "message": "Content-Type must be application/json"
            }), 400
        
        try:
            data = request.get_json()
            if data is None:
                raise BadRequest("Invalid JSON")
        except Exception:
            return jsonify({
                "error": "Bad Request",
                "message": "Invalid JSON format"
            }), 400
        
        return f(*args, **kwargs)
    return decorated_function


def validate_pagination(f):
    """Decorator to validate and sanitize pagination parameters"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))
            
            # Limit pagination to prevent abuse
            page = max(1, min(page, 1000))
            per_page = max(1, min(per_page, 100))
            
            request.validated_page = page
            request.validated_per_page = per_page
        except (ValueError, TypeError):
            page = 1
            per_page = 10
            request.validated_page = page
            request.validated_per_page = per_page
        
        return f(*args, **kwargs)
    return decorated_function
