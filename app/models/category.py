"""
Category model for organizing posts.
"""
from datetime import datetime
from app import db

class Category(db.Model):
    """Category model for organizing posts."""
    
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    color = db.Column(db.String(7))  # Hex color code
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of the Category model."""
        return f'<Category {self.name}>'
    
    def to_dict(self):
        """Convert category to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'color': self.color,
            'is_active': self.is_active,
            'post_count': self.posts.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_active_categories():
        """Get all active categories."""
        return Category.query.filter_by(is_active=True).order_by(Category.name).all()
    
    @staticmethod
    def get_category_by_slug(slug):
        """Get category by slug."""
        return Category.query.filter_by(slug=slug, is_active=True).first() 