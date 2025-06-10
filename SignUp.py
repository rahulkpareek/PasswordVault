import re
import secrets
from typing import Tuple, Optional, Dict, Any
from tinydb import TinyDB, Query
import DBhelper

class RegistrationError(Exception):
    """Custom exception for user registration operations"""
    pass

def validate_email(email: str) -> bool:
    """
    Validate email format using regex
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format, False otherwise
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if len(password) < 8:
        return (False, "Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        return (False, "Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        return (False, "Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        return (False, "Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return (False, "Password must contain at least one special character")
    
    return (True, "Password is strong")

def validate_user_input(firstname: str, lastname: str, email: str, userid: str, password: str) -> Tuple[bool, str]:
    """
    Validate all user input fields
    
    Args:
        firstname: User's first name
        lastname: User's last name
        email: User's email address
        userid: Desired user ID
        password: User's password
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    # Check for empty fields
    if not all([firstname, lastname, email, userid, password]):
        return (False, "All fields are required")
    
    # Validate first name
    if len(firstname.strip()) < 2:
        return (False, "First name must be at least 2 characters long")
    
    if not firstname.replace(' ', '').replace('-', '').replace("'", '').isalpha():
        return (False, "First name can only contain letters, spaces, hyphens, and apostrophes")
    
    # Validate last name
    if len(lastname.strip()) < 2:
        return (False, "Last name must be at least 2 characters long")
    
    if not lastname.replace(' ', '').replace('-', '').replace("'", '').isalpha():
        return (False, "Last name can only contain letters, spaces, hyphens, and apostrophes")
    
    # Validate email
    if not validate_email(email):
        return (False, "Please enter a valid email address")
    
    # Validate user ID
    if len(userid) < 3:
        return (False, "User ID must be at least 3 characters long")
    
    if len(userid) > 20:
        return (False, "User ID must be no more than 20 characters long")
    
    if not re.match(r'^[a-zA-Z0-9_]+$', userid):
        return (False, "User ID can only contain letters, numbers, and underscores")
    
    # Validate password strength
    password_valid, password_message = validate_password_strength(password)
    if not password_valid:
        return (False, password_message)
    
    return (True, "All input is valid")

def check_user_exists(db: TinyDB, userid: str, email: str) -> Tuple[bool, str]:
    """
    Check if user already exists by userid or email
    
    Args:
        db: Database connection
        userid: User ID to check
        email: Email to check
        
    Returns:
        Tuple of (exists: bool, message: str)
    """
    try:
        query = Query()
        
        # Check if userid exists
        userid_exists = db.contains(query.userid == userid)
        if userid_exists:
            return (True, f"User ID '{userid}' already exists")
        
        # Check if email exists
        email_exists = db.contains(query.email == email.lower())
        if email_exists:
            return (True, f"Email '{email}' is already registered")
        
        return (False, "User does not exist")
        
    except Exception as e:
        raise RegistrationError(f"Error checking user existence: {str(e)}")

def register_user(firstname: str, lastname: str, email: str, userid: str, password: str) -> Tuple[bool, str]:
    """
    Register a new user with comprehensive validation and security
    
    Args:
        firstname: User's first name
        lastname: User's last name
        email: User's email address
        userid: Desired user ID
        password: User's password
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Sanitize input
        firstname = firstname.strip().title()
        lastname = lastname.strip().title()
        email = email.strip().lower()
        userid = userid.strip().lower()
        
        # Validate input
        input_valid, validation_message = validate_user_input(firstname, lastname, email, userid, password)
        if not input_valid:
            return (False, validation_message)
        
        # Connect to database
        db = DBhelper.connect_to_database('users.json')
        
        # Check if user already exists
        user_exists, existence_message = check_user_exists(db, userid, email)
        if user_exists:
            return (False, existence_message)
        
        # Generate secure salt and hash password
        salt = DBhelper.generate_salt()
        password_hash = DBhelper.hash_password(password, salt)
        
        # Generate unique internal user ID
        internal_user_id = secrets.token_hex(16)
        
        # Create user record
        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "userid": userid,
            "password_hash": password_hash,
            "salt": salt,
            "internal_user_id": internal_user_id,
            "created_at": DBhelper.get_current_timestamp(),
            "is_active": True
        }
        
        # Insert user into database
        DBhelper.insert_in_db(db, user_data)
        
        # Create initial user profile in separate database
        create_user_profile(internal_user_id, firstname, lastname, email)
        
        return (True, f"User '{userid}' successfully registered")
        
    except RegistrationError as e:
        return (False, str(e))
    except Exception as e:
        return (False, f"Registration failed: {str(e)}")

def create_user_profile(internal_user_id: str, firstname: str, lastname: str, email: str) -> bool:
    """
    Create initial user profile in user info database
    
    Args:
        internal_user_id: Internal user identifier
        firstname: User's first name
        lastname: User's last name
        email: User's email
        
    Returns:
        True if successful
        
    Raises:
        RegistrationError: If profile creation fails
    """
    try:
        profile_db = DBhelper.connect_to_database('user_profiles.json')
        
        profile_data = {
            "user_id": internal_user_id,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "profile_created_at": DBhelper.get_current_timestamp(),
            "last_login": None,
            "login_count": 0
        }
        
        DBhelper.insert_in_db(profile_db, profile_data)
        return True
        
    except Exception as e:
        raise RegistrationError(f"Failed to create user profile: {str(e)}")

def update_user_info(userid: str, field: str, new_value: str) -> Tuple[bool, str]:
    """
    Update user information
    
    Args:
        userid: User ID of user to update
        field: Field to update ('firstname', 'lastname', 'email')
        new_value: New value for the field
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        allowed_fields = ['firstname', 'lastname', 'email']
        if field not in allowed_fields:
            return (False, f"Field '{field}' cannot be updated")
        
        # Validate new value based on field type
        if field in ['firstname', 'lastname']:
            if len(new_value.strip()) < 2:
                return (False, f"{field.title()} must be at least 2 characters long")
            new_value = new_value.strip().title()
        elif field == 'email':
            if not validate_email(new_value):
                return (False, "Please enter a valid email address")
            new_value = new_value.strip().lower()
        
        # Connect to database
        db = DBhelper.connect_to_database('users.json')
        
        # Check if user exists
        query = Query()
        user_data = db.get(query.userid == userid)
        if not user_data:
            return (False, f"User '{userid}' not found")
        
        # If updating email, check if new email already exists
        if field == 'email':
            email_exists = db.contains((query.email == new_value) & (query.userid != userid))
            if email_exists:
                return (False, f"Email '{new_value}' is already registered to another user")
        
        # Update user record
        db.update({field: new_value}, query.userid == userid)
        
        # Update profile database as well
        profile_db = DBhelper.connect_to_database('user_profiles.json')
        internal_user_id = user_data.get('internal_user_id')
        if internal_user_id:
            profile_query = Query()
            profile_db.update({field: new_value}, profile_query.user_id == internal_user_id)
        
        return (True, f"{field.title()} updated successfully")
        
    except Exception as e:
        return (False, f"Failed to update user info: {str(e)}")

def deactivate_user(userid: str) -> Tuple[bool, str]:
    """
    Deactivate a user account (soft delete)
    
    Args:
        userid: User ID to deactivate
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        db = DBhelper.connect_to_database('users.json')
        query = Query()
        
        # Check if user exists
        user_data = db.get(query.userid == userid)
        if not user_data:
            return (False, f"User '{userid}' not found")
        
        # Deactivate user
        db.update({
            'is_active': False,
            'deactivated_at': DBhelper.get_current_timestamp()
        }, query.userid == userid)
        
        return (True, f"User '{userid}' has been deactivated")
        
    except Exception as e:
        return (False, f"Failed to deactivate user: {str(e)}")

def get_user_info(userid: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Get user information by userid
    
    Args:
        userid: User ID to look up
        
    Returns:
        Tuple of (success: bool, message: str, user_data: Optional[Dict])
    """
    try:
        db = DBhelper.connect_to_database('users.json')
        query = Query()
        
        user_data = db.get(query.userid == userid)
        if not user_data:
            return (False, f"User '{userid}' not found", None)
        
        # Remove sensitive information before returning
        safe_user_data = {
            'firstname': user_data.get('firstname'),
            'lastname': user_data.get('lastname'),
            'email': user_data.get('email'),
            'userid': user_data.get('userid'),
            'created_at': user_data.get('created_at'),
            'is_active': user_data.get('is_active', True)
        }
        
        return (True, "User information retrieved successfully", safe_user_data)
        
    except Exception as e:
        return (False, f"Failed to get user info: {str(e)}", None)

# Legacy function for backward compatibility
def RegisterUser(firstname: str, lastname: str, email: str, userid: str, password: str) -> Tuple[bool, str]:
    """
    Legacy function for backward compatibility
    
    Args:
        firstname: User's first name
        lastname: User's last name (note: fixed typo from 'lasttname')
        email: User's email address
        userid: Desired user ID
        password: User's password
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    return register_user(firstname, lastname, email, userid, password)
