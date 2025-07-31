"""
Authentication blueprint for user login, registration, and profile management.
"""
from flask import Blueprint

# Create auth blueprint
auth_bp = Blueprint('auth', __name__)

# Import routes after creating blueprint to avoid circular imports
from . import routes 