"""
Views package for main application routes.
"""
from flask import Blueprint

# Create main blueprint
main_bp = Blueprint('main', __name__)

# Import routes after creating blueprint to avoid circular imports
from . import routes 