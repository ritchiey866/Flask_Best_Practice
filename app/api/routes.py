"""
API routes for RESTful endpoints.
"""
from flask import jsonify, request, abort
from flask_login import login_required, current_user
from app.api import api_bp
from app.models import User, Post, Category
from app import db

# API Response Helpers
def api_response(data=None, message="", status_code=200):
    """Helper function to create consistent API responses."""
    response = {
        "success": 200 <= status_code < 300,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def api_error(message="An error occurred", status_code=400):
    """Helper function to create error responses."""
    return api_response(message=message, status_code=status_code)

# User API Endpoints
@api_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    users = User.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    data = {
        'users': [user.to_dict() for user in users.items],
        'pagination': {
            'page': users.page,
            'pages': users.pages,
            'per_page': users.per_page,
            'total': users.total,
            'has_next': users.has_next,
            'has_prev': users.has_prev
        }
    }
    
    return api_response(data=data, message="Users retrieved successfully")

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user."""
    user = User.query.get_or_404(user_id)
    return api_response(data=user.to_dict(), message="User retrieved successfully")

@api_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json()
    
    if not data:
        return api_error("No data provided", 400)
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return api_error(f"Missing required field: {field}", 400)
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return api_error("Username already exists", 409)
    
    if User.query.filter_by(email=data['email']).first():
        return api_error("Email already registered", 409)
    
    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        bio=data.get('bio')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return api_response(data=user.to_dict(), message="User created successfully", status_code=201)

# Post API Endpoints
@api_bp.route('/posts', methods=['GET'])
def get_posts():
    """Get all posts."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    author_id = request.args.get('author_id', type=int)
    published_only = request.args.get('published_only', 'true').lower() == 'true'
    
    query = Post.query
    
    if published_only:
        query = query.filter_by(is_published=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if author_id:
        query = query.filter_by(author_id=author_id)
    
    posts = query.order_by(Post.created_at.desc()).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    data = {
        'posts': [post.to_dict() for post in posts.items],
        'pagination': {
            'page': posts.page,
            'pages': posts.pages,
            'per_page': posts.per_page,
            'total': posts.total,
            'has_next': posts.has_next,
            'has_prev': posts.has_prev
        }
    }
    
    return api_response(data=data, message="Posts retrieved successfully")

@api_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post."""
    post = Post.query.get_or_404(post_id)
    
    # Increment view count
    post.increment_view_count()
    
    return api_response(data=post.to_dict(), message="Post retrieved successfully")

@api_bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    """Create a new post."""
    data = request.get_json()
    
    if not data:
        return api_error("No data provided", 400)
    
    # Validate required fields
    required_fields = ['title', 'content']
    for field in required_fields:
        if field not in data:
            return api_error(f"Missing required field: {field}", 400)
    
    # Create post
    post = Post(
        title=data['title'],
        content=data['content'],
        excerpt=data.get('excerpt'),
        author_id=current_user.id,
        category_id=data.get('category_id'),
        is_published=data.get('is_published', False),
        is_featured=data.get('is_featured', False)
    )
    
    # Generate slug
    from app.utils import generate_slug
    post.slug = generate_slug(post.title)
    
    db.session.add(post)
    db.session.commit()
    
    return api_response(data=post.to_dict(), message="Post created successfully", status_code=201)

# Category API Endpoints
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories."""
    categories = Category.get_active_categories()
    data = [category.to_dict() for category in categories]
    
    return api_response(data=data, message="Categories retrieved successfully")

@api_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a specific category."""
    category = Category.query.get_or_404(category_id)
    return api_response(data=category.to_dict(), message="Category retrieved successfully")

# Search API Endpoint
@api_bp.route('/search', methods=['GET'])
def search_posts():
    """Search posts."""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if not query:
        return api_error("Search query is required", 400)
    
    posts = Post.search_posts(query, page=page, per_page=per_page)
    
    data = {
        'posts': [post.to_dict() for post in posts.items],
        'query': query,
        'pagination': {
            'page': posts.page,
            'pages': posts.pages,
            'per_page': posts.per_page,
            'total': posts.total,
            'has_next': posts.has_next,
            'has_prev': posts.has_prev
        }
    }
    
    return api_response(data=data, message="Search completed successfully") 