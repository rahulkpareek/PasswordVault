import tkinter as tk
import tkinter.messagebox as messagebox
from typing import Tuple, Optional, Callable
import logging
from functools import wraps
import SignIn
import SignUp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('password_vault.log'),
        logging.StreamHandler()
    ]
)

class HandlerError(Exception):
    """Custom exception for handler operations"""
    pass

def handle_exceptions(func: Callable) -> Callable:
    """
    Decorator to handle exceptions in handler functions
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function with exception handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            messagebox.showerror("System Error", f"An unexpected error occurred: {str(e)}")
            return False
    return wrapper

def validate_input_length(text: str, field_name: str, min_length: int = 1, max_length: int = 100) -> Tuple[bool, str]:
    """
    Validate input field length
    
    Args:
        text: Text to validate
        field_name: Name of the field for error messages
        min_length: Minimum required length
        max_length: Maximum allowed length
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    if not text or len(text.strip()) < min_length:
        return (False, f"{field_name} cannot be empty")
    
    if len(text.strip()) > max_length:
        return (False, f"{field_name} cannot exceed {max_length} characters")
    
    return (True, "")

def sanitize_input(text: str) -> str:
    """
    Sanitize user input by trimming whitespace
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    return text.strip() if text else ""

@handle_exceptions
def sign_in_handler(username: str, password: str, success_callback: Optional[Callable] = None) -> bool:
    """
    Handle user sign-in with comprehensive validation
    
    Args:
        username: Username for authentication
        password: Password for authentication
        success_callback: Optional callback function to execute on successful login
        
    Returns:
        True if sign-in successful, False otherwise
    """
    try:
        # Sanitize inputs
        username = sanitize_input(username)
        password = sanitize_input(password)
        
        # Validate username
        username_valid, username_error = validate_input_length(username, "Username", min_length=3, max_length=50)
        if not username_valid:
            messagebox.showwarning("Input Error", username_error)
            logging.warning(f"Sign-in attempt with invalid username: {username_error}")
            return False
        
        # Validate password
        password_valid, password_error = validate_input_length(password, "Password", min_length=1, max_length=200)
        if not password_valid:
            messagebox.showwarning("Input Error", password_error)
            logging.warning(f"Sign-in attempt with invalid password for user: {username}")
            return False
        
        # Attempt sign-in
        logging.info(f"Sign-in attempt for user: {username}")
        success, message = SignIn.try_signing_in(username, password)
        
        if success:
            messagebox.showinfo("Success", message)
            logging.info(f"Successful sign-in for user: {username}")
            
            # Execute success callback if provided
            if success_callback:
                success_callback(username)
            else:
                # Default behavior - display user info
                display_result = SignIn.display_user_info(username, password)
                if not display_result[0]:
                    messagebox.showwarning("Warning", f"Login successful but failed to load user info: {display_result[1]}")
            
            return True
        else:
            messagebox.showerror("Authentication Error", message)
            logging.warning(f"Failed sign-in attempt for user: {username} - {message}")
            return False
            
    except Exception as e:
        error_msg = f"Sign-in failed due to system error: {str(e)}"
        messagebox.showerror("System Error", error_msg)
        logging.error(f"System error during sign-in for user {username}: {str(e)}")
        return False

@handle_exceptions
def registration_handler(firstname: str, lastname: str, email: str, userid: str, 
                        password: str, confirm_password: str, success_callback: Optional[Callable] = None) -> bool:
    """
    Handle user registration with comprehensive validation
    
    Args:
        firstname: User's first name
        lastname: User's last name
        email: User's email address
        userid: Desired user ID
        password: User's password
        confirm_password: Password confirmation
        success_callback: Optional callback function to execute on successful registration
        
    Returns:
        True if registration successful, False otherwise
    """
    try:
        # Sanitize inputs
        firstname = sanitize_input(firstname)
        lastname = sanitize_input(lastname)
        email = sanitize_input(email)
        userid = sanitize_input(userid)
        password = sanitize_input(password)
        confirm_password = sanitize_input(confirm_password)
        
        # Validate all fields
        validation_checks = [
            (firstname, "First name", 2, 50),
            (lastname, "Last name", 2, 50),
            (email, "Email", 5, 100),
            (userid, "User ID", 3, 20),
            (password, "Password", 8, 200),
            (confirm_password, "Confirm password", 8, 200)
        ]
        
        for field_value, field_name, min_len, max_len in validation_checks:
            field_valid, field_error = validate_input_length(field_value, field_name, min_len, max_len)
            if not field_valid:
                messagebox.showwarning("Input Error", field_error)
                logging.warning(f"Registration attempt with invalid {field_name.lower()}")
                return False
        
        # Check password confirmation
        if password != confirm_password:
            messagebox.showwarning("Input Error", "Passwords do not match")
            logging.warning(f"Registration attempt with mismatched passwords for user: {userid}")
            return False
        
        # Attempt registration
        logging.info(f"Registration attempt for user: {userid}")
        success, message = SignUp.register_user(firstname, lastname, email, userid, password)
        
        if success:
            messagebox.showinfo("Success", message)
            logging.info(f"Successful registration for user: {userid}")
            
            # Execute success callback if provided
            if success_callback:
                success_callback(userid)
            
            return True
        else:
            messagebox.showerror("Registration Error", message)
            logging.warning(f"Failed registration attempt for user: {userid} - {message}")
            return False
            
    except Exception as e:
        error_msg = f"Registration failed due to system error: {str(e)}"
        messagebox.showerror("System Error", error_msg)
        logging.error(f"System error during registration for user {userid}: {str(e)}")
        return False

@handle_exceptions
def change_password_handler(username: str, current_password: str, new_password: str, 
                           confirm_new_password: str) -> bool:
    """
    Handle password change requests
    
    Args:
        username: Username
        current_password: Current password
        new_password: New password
        confirm_new_password: New password confirmation
        
    Returns:
        True if password change successful, False otherwise
    """
    try:
        # Sanitize inputs
        username = sanitize_input(username)
        current_password = sanitize_input(current_password)
        new_password = sanitize_input(new_password)
        confirm_new_password = sanitize_input(confirm_new_password)
        
        # Validate inputs
        if not all([username, current_password, new_password, confirm_new_password]):
            messagebox.showwarning("Input Error", "All fields are required")
            return False
        
        # Check new password confirmation
        if new_password != confirm_new_password:
            messagebox.showwarning("Input Error", "New passwords do not match")
            return False
        
        # Attempt password change
        logging.info(f"Password change attempt for user: {username}")
        success, message = SignIn.change_password(username, current_password, new_password)
        
        if success:
            messagebox.showinfo("Success", message)
            logging.info(f"Successful password change for user: {username}")
            return True
        else:
            messagebox.showerror("Error", message)
            logging.warning(f"Failed password change attempt for user: {username} - {message}")
            return False
            
    except Exception as e:
        error_msg = f"Password change failed due to system error: {str(e)}"
        messagebox.showerror("System Error", error_msg)
        logging.error(f"System error during password change for user {username}: {str(e)}")
        return False

@handle_exceptions
def update_user_info_handler(userid: str, field: str, new_value: str) -> bool:
    """
    Handle user information updates
    
    Args:
        userid: User ID
        field: Field to update
        new_value: New value for the field
        
    Returns:
        True if update successful, False otherwise
    """
    try:
        # Sanitize inputs
        userid = sanitize_input(userid)
        new_value = sanitize_input(new_value)
        
        if not userid or not new_value:
            messagebox.showwarning("Input Error", "User ID and new value cannot be empty")
            return False
        
        # Attempt update
        logging.info(f"User info update attempt for user: {userid}, field: {field}")
        success, message = SignUp.update_user_info(userid, field, new_value)
        
        if success:
            messagebox.showinfo("Success", message)
            logging.info(f"Successful user info update for user: {userid}")
            return True
        else:
            messagebox.showerror("Error", message)
            logging.warning(f"Failed user info update for user: {userid} - {message}")
            return False
            
    except Exception as e:
        error_msg = f"User info update failed due to system error: {str(e)}"
        messagebox.showerror("System Error", error_msg)
        logging.error(f"System error during user info update for user {userid}: {str(e)}")
        return False

# Legacy function for backward compatibility
def SignInHandler(username: str, password: str) -> bool:
    """
    Legacy function for backward compatibility
    
    Args:
        username: Username for authentication
        password: Password for authentication
        
    Returns:
        True if sign-in successful, False otherwise
    """
    return sign_in_handler(username, password)

def SubmitDetails(firstname: str, lastname: str, email: str, userid: str, 
                 password: str, repassword: str) -> bool:
    """
    Legacy function for backward compatibility
    
    Args:
        firstname: User's first name
        lastname: User's last name (fixed typo from original)
        email: User's email address
        userid: Desired user ID
        password: User's password
        repassword: Password confirmation
        
    Returns:
        True if registration successful, False otherwise
    """
    return registration_handler(firstname, lastname, email, userid, password, repassword)
