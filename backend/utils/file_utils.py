"""
File Utility Functions
Enterprise-level file operations and validation
"""

import os
import re
from pathlib import Path
from typing import Optional
from fastapi import HTTPException


def validate_filename(filename: str, allowed_extensions: Optional[list] = None) -> str:
    """
    Validate and sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: The filename to validate
        allowed_extensions: List of allowed file extensions (e.g., ['.pdf', '.xlsx'])
        
    Returns:
        Sanitized filename
        
    Raises:
        HTTPException: If filename is invalid
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename cannot be empty")
    
    # Remove any path components
    filename = os.path.basename(filename)
    
    # Remove any null bytes
    filename = filename.replace('\x00', '')
    
    # Validate file extension if specified
    if allowed_extensions:
        if not any(filename.lower().endswith(ext.lower()) for ext in allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed extensions: {', '.join(allowed_extensions)}"
            )
    
    # Check for dangerous characters and path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename. Path traversal not allowed"
        )
    
    # Validate filename contains only safe characters
    if not re.match(r'^[a-zA-Z0-9\s,\-_.()]+$', filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid filename. Contains unsafe characters"
        )
    
    # Limit filename length
    if len(filename) > 255:
        raise HTTPException(
            status_code=400,
            detail="Filename too long. Maximum 255 characters"
        )
    
    return filename


def sanitize_path(file_path: str, base_directory: str) -> Path:
    """
    Sanitize and validate file path to ensure it's within base directory.
    
    Args:
        file_path: File path to sanitize
        base_directory: Base directory that file must be within
        
    Returns:
        Resolved Path object
        
    Raises:
        HTTPException: If path is outside base directory
    """
    base_dir = Path(base_directory).resolve()
    file_path_resolved = Path(file_path).resolve()
    
    # Security check: ensure path is within base directory
    try:
        if not str(file_path_resolved).startswith(str(base_dir)):
            raise HTTPException(
                status_code=403,
                detail="Access denied. Path traversal detected"
            )
    except (OSError, ValueError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file path: {str(e)}"
        )
    
    return file_path_resolved

