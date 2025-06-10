import hashlib
import secrets
import os
from typing import Tuple, Optional, Dict, Any
from tinydb import TinyDB, Query
import DBhelper

class AuthenticationError(Exception):
    """Custom exception for authentication operations"""
    pass

def check_username_exists(db: TinyDB, username: str) -> Optional[Dict]:
    """
    Check if username exists in database
    
    Args:
        db: Database connection
        username: Username to check
        
    Returns:
        User data if found, None otherwise
    """
    return DBhelper.search_db(db, 'username', username)

def get_user_info(db: TinyDB, user_id: str) -> Optional[Dict]:
    """
    Get user information from database
    
    Args:
        db: Database connection
        user_id: User identifier
        
    Returns:
        User info if found, None otherwise
    """
    return DBhelper.search_db(db, 'user_id', user_id)

def create_user(username: str, password: str) -> Tuple[bool, str]:
    """
    Create a new user account
    
    Args:
        username: Username for new account
        password: Password for new account
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Input validation
        if not username or not password:
            return (False, "Username and password cannot be empty")
        
        if len(username) < 3:
            return (False, "Username must be at least 3 characters long")
        
        if len(password) < 8:
            return (False, "Password must be at least 8 characters long")
        
        db = DBhelper.connect_to_database('users.json')
        
        # Check if user already exists
        if check_username_exists(db, username):
            return (False, f"User '{username}' already exists")
        
        # Generate salt and hash password
        salt = DBhelper.generate_salt()
        password_hash = DBhelper.hash_password(password, salt)
        
        # Generate unique user ID
        user_id = secrets.token_hex(16)
        
        # Create user record
        user_data = {
            'username': username,
            'password_hash': password_hash,
            'salt': salt,
            'user_id': user_id
        }
        
        DBhelper.insert_in_db(db, user_data)
        return (True, "User created successfully")
        
    except Exception as e:
        return (False, f"Failed to create user: {str(e)}")

def try_signing_in(username: str, password: str) -> Tuple[bool, str]:
    """
    Attempt to sign in user with username and password
    
    Args:
        username: Username to authenticate
        password: Password to verify
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Input validation
        if not username or not password:
            return (False, "Username and password cannot be empty")
        
        db = DBhelper.connect_to_database('users.json')
        user_data = check_username_exists(db, username)
        
        if not user_data:
            return (False, f"User '{username}' doesn't exist")
        
        # Verify password using stored salt
        stored_hash = user_data.get('password_hash')
        salt = user_data.get('salt')
        
        if not stored_hash or not salt:
            return (False, "Invalid user data in database")
        
        # Hash provided password with stored salt
        password_hash = DBhelper.hash_password(password, salt)
        
        if password_hash == stored_hash:
            return (True, "Login successful")
        else:
            return (False, "Invalid password")
            
    except Exception as e:
        return (False, f"Authentication failed: {str(e)}")

def display_user_info(username: str, password: str, output_file: str = "user_info.txt") -> Tuple[bool, str]:
    """
    Display user information after authentication
    
    Args:
        username: Username to authenticate
        password: Password to verify
        output_file: File to write user info to
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # First authenticate user
        auth_success, auth_message = try_signing_in(username, password)
        if not auth_success:
            return (False, f"Authentication failed: {auth_message}")
        
        # Get user info from info database
        info_db = DBhelper.connect_to_database('user_info.json')
        
        # Get user data to find user_id
        users_db = DBhelper.connect_to_database('users.json')
        user_data = check_username_exists(users_db, username)
        
        if not user_data:
            return (False, "User data not found")
        
        user_id = user_data.get('user_id')
        user_info = get_user_info(info_db, user_id)
        
        # Write info to file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(f"User Information for: {username}\n")
            file.write("=" * 40 + "\n")
            
            if user_info:
                for key, value in user_info.items():
                    if key != 'user_id':  # Don't display internal ID
                        file.write(f"{key.title()}: {value}\n")
            else:
                file.write("No additional user information found.\n")
        
        return (True, f"User information written to {output_file}")
        
    except Exception as e:
        return (False, f"Failed to display user info: {str(e)}")

def change_password(username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
    """
    Change user password
    
    Args:
        username: Username
        old_password: Current password
        new_password: New password
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Validate new password
        if len(new_password) < 8:
            return (False, "New password must be at least 8 characters long")
        
        # Authenticate with old password
        auth_success, auth_message = try_signing_in(username, old_password)
        if not auth_success:
            return (False, f"Authentication failed: {auth_message}")
        
        db = DBhelper.connect_to_database('users.json')
        
        # Generate new salt and hash
        new_salt = DBhelper.generate_salt()
        new_password_hash = DBhelper.hash_password(new_password, new_salt)
        
        # Update user record
        query = DBhelper.make_query()
        db.update({
            'password_hash': new_password_hash,
            'salt': new_salt
        }, query.username == username)
        
        return (True, "Password changed successfully")
        
    except Exception as e:
        return (False, f"Failed to change password: {str(e)}")
