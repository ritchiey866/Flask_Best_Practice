"""
Utility helper functions.
"""
import re
import unicodedata
from datetime import datetime

def generate_slug(text):
    """
    Generate a URL-friendly slug from text.
    
    Args:
        text (str): The text to convert to a slug
        
    Returns:
        str: URL-friendly slug
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Convert to lowercase and replace spaces with hyphens
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    text = re.sub(r'[-\s]+', '-', text)
    
    return text

def format_date(date, format_string='%B %d, %Y'):
    """
    Format a datetime object to a readable string.
    
    Args:
        date (datetime): The datetime object to format
        format_string (str): The format string to use
        
    Returns:
        str: Formatted date string
    """
    if not date:
        return ''
    
    if isinstance(date, str):
        try:
            date = datetime.fromisoformat(date.replace('Z', '+00:00'))
        except ValueError:
            return date
    
    return date.strftime(format_string)

def truncate_text(text, length=100, suffix='...'):
    """
    Truncate text to a specified length.
    
    Args:
        text (str): The text to truncate
        length (int): Maximum length
        suffix (str): Suffix to add if text is truncated
        
    Returns:
        str: Truncated text
    """
    if not text:
        return ''
    
    if len(text) <= length:
        return text
    
    return text[:length].rsplit(' ', 1)[0] + suffix

def allowed_file(filename, allowed_extensions):
    """
    Check if a file has an allowed extension.
    
    Args:
        filename (str): The filename to check
        allowed_extensions (set): Set of allowed file extensions
        
    Returns:
        bool: True if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_extension(filename):
    """
    Get the file extension from a filename.
    
    Args:
        filename (str): The filename
        
    Returns:
        str: File extension (without the dot)
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''

def sanitize_filename(filename):
    """
    Sanitize a filename for safe storage.
    
    Args:
        filename (str): The original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove or replace unsafe characters
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.strip('-')

def get_pagination_info(pagination):
    """
    Get pagination information for templates.
    
    Args:
        pagination: SQLAlchemy pagination object
        
    Returns:
        dict: Pagination information
    """
    return {
        'page': pagination.page,
        'pages': pagination.pages,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'next_num': pagination.next_num,
        'prev_num': pagination.prev_num,
        'iter_pages': pagination.iter_pages()
    } 