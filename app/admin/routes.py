"""
Admin routes for administrative functions.
"""
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.admin import admin_bp
from app.models import User, Post, Category
from app import db

def admin_required(f):
    """Decorator to require admin privileges."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard."""
    # Get statistics
    total_users = User.query.count()
    total_posts = Post.query.count()
    published_posts = Post.query.filter_by(is_published=True).count()
    total_categories = Category.query.count()
    
    # Get recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    stats = {
        'total_users': total_users,
        'total_posts': total_posts,
        'published_posts': published_posts,
        'total_categories': total_categories
    }
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_users=recent_users,
                         recent_posts=recent_posts)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Admin users management."""
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status."""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'error')
        return redirect(url_for('admin.users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}.', 'success')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_user_admin(user_id):
    """Toggle user admin privileges."""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'error')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'granted admin privileges' if user.is_admin else 'revoked admin privileges'
    flash(f'User {user.username} has been {status}.', 'success')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/posts')
@login_required
@admin_required
def posts():
    """Admin posts management."""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/posts.html', posts=posts)

@admin_bp.route('/posts/<int:post_id>/toggle-published', methods=['POST'])
@login_required
@admin_required
def toggle_post_published(post_id):
    """Toggle post published status."""
    post = Post.query.get_or_404(post_id)
    
    post.is_published = not post.is_published
    db.session.commit()
    
    status = 'published' if post.is_published else 'unpublished'
    flash(f'Post "{post.title}" has been {status}.', 'success')
    
    return redirect(url_for('admin.posts'))

@admin_bp.route('/posts/<int:post_id>/toggle-featured', methods=['POST'])
@login_required
@admin_required
def toggle_post_featured(post_id):
    """Toggle post featured status."""
    post = Post.query.get_or_404(post_id)
    
    post.is_featured = not post.is_featured
    db.session.commit()
    
    status = 'featured' if post.is_featured else 'unfeatured'
    flash(f'Post "{post.title}" has been {status}.', 'success')
    
    return redirect(url_for('admin.posts'))

@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """Admin categories management."""
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_category():
    """Create a new category."""
    from app.forms import CategoryForm
    
    form = CategoryForm()
    if form.validate_on_submit():
        from app.utils import generate_slug
        
        category = Category(
            name=form.name.data,
            slug=generate_slug(form.name.data),
            description=form.description.data,
            color=form.color.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/create_category.html', form=form)

@admin_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    """Edit a category."""
    from app.forms import CategoryForm
    
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        from app.utils import generate_slug
        
        category.name = form.name.data
        category.slug = generate_slug(form.name.data)
        category.description = form.description.data
        category.color = form.color.data
        
        db.session.commit()
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/edit_category.html', form=form, category=category)

@admin_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    """Delete a category."""
    category = Category.query.get_or_404(category_id)
    
    # Check if category has posts
    if category.posts.count() > 0:
        flash('Cannot delete category with existing posts.', 'error')
        return redirect(url_for('admin.categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin.categories')) 