from tinydb import TinyDB, Query
import hashlib
import secrets
import os
from typing import Optional, Dict, Any, Union
from datetime import datetime

class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass

def connect_to_database(dbfile: str) -> TinyDB:
    """
    Connect to TinyDB database with proper error handling
    
    Args:
        dbfile: Path to the database file
        
    Returns:
        TinyDB connection object
        
    Raises:
        DatabaseError: If connection fails
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(dbfile) if os.path.dirname(dbfile) else '.', exist_ok=True)
        return TinyDB(dbfile)
    except Exception as e:
        raise DatabaseError(f"Failed to connect to database {dbfile}: {str(e)}")

def generate_salt() -> str:
    """Generate a cryptographically secure random salt"""
    return secrets.token_hex(32)

def hash_password(password: str, salt: str) -> str:
    """
    Hash password with salt using SHA-256
    
    Args:
        password: Plain text password
        salt: Random salt string
        
    Returns:
        Hexadecimal hash string
    """
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def encrypt_string(input_string: str) -> str:
    """
    Hash a string using SHA-256
    
    Args:
        input_string: String to hash
        
    Returns:
        Hexadecimal hash string
    """
    return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

def search_db(db: TinyDB, field: str, value: Any) -> Optional[Dict]:
    """
    Search database for a record matching field=value
    
    Args:
        db: TinyDB connection
        field: Field name to search
        value: Value to match
        
    Returns:
        Dictionary if found, None otherwise
        
    Raises:
        DatabaseError: If search operation fails
    """
    try:
        query = Query()
        result = db.get(query[field] == value)
        return result
    except Exception as e:
        raise DatabaseError(f"Search operation failed: {str(e)}")

def insert_in_db(db: TinyDB, data: Dict) -> bool:
    """
    Insert data into database
    
    Args:
        db: TinyDB connection
        data: Dictionary to insert
        
    Returns:
        True if successful
        
    Raises:
        DatabaseError: If insert operation fails
    """
    try:
        db.insert(data)
        return True
    except Exception as e:
        raise DatabaseError(f"Insert operation failed: {str(e)}")

def delete_from_db(db: TinyDB, query: Query) -> bool:
    """
    Delete records matching query from database
    
    Args:
        db: TinyDB connection
        query: TinyDB Query object
        
    Returns:
        True if successful
        
    Raises:
        DatabaseError: If delete operation fails
    """
    try:
        removed_count = len(db.remove(query))
        return removed_count > 0
    except Exception as e:
        raise DatabaseError(f"Delete operation failed: {str(e)}")

def delete_all_from_db(db: TinyDB) -> bool:
    """
    Delete all records from database
    
    Args:
        db: TinyDB connection
        
    Returns:
        True if successful
        
    Raises:
        DatabaseError: If truncate operation fails
    """
    try:
        db.truncate()
        return True
    except Exception as e:
        raise DatabaseError(f"Truncate operation failed: {str(e)}")

def make_query() -> Query:
    """Create and return a new Query object"""
    return Query()

def get_current_timestamp() -> str:
    """
    Get current timestamp as ISO format string
    
    Returns:
        Current timestamp as string
    """
    return datetime.now().isoformat()
