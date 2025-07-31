"""
Main application routes.
"""
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.views import main_bp
from app.models import Post, Category, User
from app import db

@main_bp.route('/')
def index():
    """Home page route."""
    page = request.args.get('page', 1, type=int)
    posts = Post.get_published_posts(page=page, per_page=6)
    featured_posts = Post.get_featured_posts(limit=3)
    categories = Category.get_active_categories()
    
    return render_template('main/index.html',
                         posts=posts,
                         featured_posts=featured_posts,
                         categories=categories)

@main_bp.route('/about')
def about():
    """About page route."""
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """Contact page route."""
    return render_template('main/contact.html')

@main_bp.route('/posts')
def posts():
    """Posts listing page."""
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category')
    
    if category_slug:
        category = Category.get_category_by_slug(category_slug)
        if not category:
            abort(404)
        posts = Post.query.filter_by(category_id=category.id, is_published=True)\
                         .order_by(Post.created_at.desc())\
                         .paginate(page=page, per_page=10, error_out=False)
    else:
        posts = Post.get_published_posts(page=page, per_page=10)
        category = None
    
    categories = Category.get_active_categories()
    
    return render_template('main/posts.html',
                         posts=posts,
                         category=category,
                         categories=categories)

@main_bp.route('/post/<slug>')
def post_detail(slug):
    """Individual post detail page."""
    post = Post.query.filter_by(slug=slug, is_published=True).first()
    if not post:
        abort(404)
    
    # Increment view count
    post.increment_view_count()
    
    # Get related posts
    related_posts = Post.query.filter(
        Post.category_id == post.category_id,
        Post.id != post.id,
        Post.is_published == True
    ).limit(3).all()
    
    return render_template('main/post_detail.html',
                         post=post,
                         related_posts=related_posts)

@main_bp.route('/search')
def search():
    """Search posts."""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return redirect(url_for('main.index'))
    
    posts = Post.search_posts(query, page=page, per_page=10)
    
    return render_template('main/search.html',
                         posts=posts,
                         query=query)

@main_bp.route('/author/<username>')
def author_posts(username):
    """Show posts by a specific author."""
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author_id=user.id, is_published=True)\
                     .order_by(Post.created_at.desc())\
                     .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('main/author_posts.html',
                         user=user,
                         posts=posts)

@main_bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new post."""
    from app.forms import PostForm
    
    form = PostForm()
    categories = Category.get_active_categories()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            excerpt=form.excerpt.data,
            author_id=current_user.id,
            category_id=form.category_id.data if form.category_id.data else None,
            is_published=form.is_published.data
        )
        
        # Generate slug from title
        from app.utils import generate_slug
        post.slug = generate_slug(post.title)
        
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('main.post_detail', slug=post.slug))
    
    return render_template('main/create_post.html', form=form)

@main_bp.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit an existing post."""
    from app.forms import PostForm
    
    post = Post.query.get_or_404(post_id)
    
    # Check if user can edit this post
    if post.author_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    form = PostForm(obj=post)
    categories = Category.get_active_categories()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.excerpt = form.excerpt.data
        post.category_id = form.category_id.data if form.category_id.data else None
        post.is_published = form.is_published.data
        
        # Update slug if title changed
        from app.utils import generate_slug
        post.slug = generate_slug(post.title)
        
        db.session.commit()
        
        flash('Post updated successfully!', 'success')
        return redirect(url_for('main.post_detail', slug=post.slug))
    
    return render_template('main/edit_post.html', form=form, post=post)

@main_bp.route('/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a post."""
    post = Post.query.get_or_404(post_id)
    
    # Check if user can delete this post
    if post.author_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('main.index')) 