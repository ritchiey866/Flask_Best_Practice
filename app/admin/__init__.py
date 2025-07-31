"""
Admin blueprint for administrative functions.
"""
from flask import Blueprint

# Create admin blueprint
admin_bp = Blueprint('admin', __name__)

# Import routes after creating blueprint to avoid circular imports
from . import routes 