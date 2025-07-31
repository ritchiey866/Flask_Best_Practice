"""
Post model for blog posts and content management.
"""
from datetime import datetime
from app import db

class Post(db.Model):
    """Post model for blog posts and content management."""
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(200))
    is_published = db.Column(db.Boolean, default=False, index=True)
    is_featured = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Relationships
    category = db.relationship('Category', backref='posts')
    
    def __repr__(self):
        """String representation of the Post model."""
        return f'<Post {self.title}>'
    
    def to_dict(self):
        """Convert post to dictionary for API responses."""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'excerpt': self.excerpt,
            'featured_image': self.featured_image,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
            'view_count': self.view_count,
            'author': self.author.to_dict() if self.author else None,
            'category': self.category.to_dict() if self.category else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
    
    def increment_view_count(self):
        """Increment the view count for this post."""
        self.view_count += 1
        db.session.commit()
    
    @staticmethod
    def get_published_posts(page=1, per_page=10):
        """Get paginated published posts."""
        return Post.query.filter_by(is_published=True)\
                        .order_by(Post.created_at.desc())\
                        .paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def get_featured_posts(limit=5):
        """Get featured posts."""
        return Post.query.filter_by(is_published=True, is_featured=True)\
                        .order_by(Post.created_at.desc())\
                        .limit(limit).all()
    
    @staticmethod
    def search_posts(query, page=1, per_page=10):
        """Search posts by title and content."""
        search_term = f"%{query}%"
        return Post.query.filter(
            Post.is_published == True,
            db.or_(
                Post.title.ilike(search_term),
                Post.content.ilike(search_term)
            )
        ).order_by(Post.created_at.desc())\
         .paginate(page=page, per_page=per_page, error_out=False) 