"""
Admin Routes - Content Management
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Category, SubCategory, Article, Tag
from datetime import datetime
import re

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text

# ==========================================
# Dashboard
# ==========================================

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard with statistics"""
    stats = {
        'total_categories': Category.query.count(),
        'total_subcategories': SubCategory.query.count(),
        'total_tags': Tag.query.count(),
        'total_articles': Article.query.count(),
        'published_articles': Article.query.filter_by(is_published=True).count(),
        'draft_articles': Article.query.filter_by(is_published=False).count(),
        'featured_articles': Article.query.filter_by(is_featured=True).count(),
    }
    
    recent_articles = Article.query.order_by(Article.updated_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_articles=recent_articles)

# ==========================================
# Category Management
# ==========================================

@admin_bp.route('/categories')
@login_required
def categories():
    """List all categories"""
    categories = Category.query.order_by(Category.order, Category.name).all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def category_new():
    """Create new category"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        order = request.form.get('order', 0, type=int)
        
        if not name:
            flash('Category name is required', 'error')
            return redirect(url_for('admin.category_new'))
        
        slug = slugify(name)
        
        # Check if slug already exists
        if Category.query.filter_by(slug=slug).first():
            flash('A category with this name already exists', 'error')
            return redirect(url_for('admin.category_new'))
        
        category = Category(
            name=name,
            slug=slug,
            description=description,
            order=order
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash(f'Category "{name}" created successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', category=None)

@admin_bp.route('/category/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def category_edit(id):
    """Edit existing category"""
    category = Category.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        order = request.form.get('order', 0, type=int)
        
        if not name:
            flash('Category name is required', 'error')
            return redirect(url_for('admin.category_edit', id=id))
        
        slug = slugify(name)
        
        # Check if slug exists (excluding current category)
        existing = Category.query.filter_by(slug=slug).first()
        if existing and existing.id != id:
            flash('A category with this name already exists', 'error')
            return redirect(url_for('admin.category_edit', id=id))
        
        category.name = name
        category.slug = slug
        category.description = description
        category.order = order
        category.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash(f'Category "{name}" updated successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', category=category)

@admin_bp.route('/category/<int:id>/delete', methods=['POST'])
@login_required
def category_delete(id):
    """Delete category"""
    category = Category.query.get_or_404(id)
    
    # Check if category has articles
    if category.articles.count() > 0:
        flash(f'Cannot delete category "{category.name}" because it has articles', 'error')
        return redirect(url_for('admin.categories'))
    
    name = category.name
    db.session.delete(category)
    db.session.commit()
    
    flash(f'Category "{name}" deleted successfully!', 'success')
    return redirect(url_for('admin.categories'))

# ==========================================
# SubCategory Management
# ==========================================

@admin_bp.route('/subcategories')
@login_required
def subcategories():
    """List all subcategories"""
    subcategories = SubCategory.query.join(Category).order_by(
        Category.name, SubCategory.order, SubCategory.name
    ).all()
    return render_template('admin/subcategories.html', subcategories=subcategories)

@admin_bp.route('/subcategory/new', methods=['GET', 'POST'])
@login_required
def subcategory_new():
    """Create new subcategory"""
    categories = Category.query.order_by(Category.name).all()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category_id = request.form.get('category_id', type=int)
        order = request.form.get('order', 0, type=int)
        
        if not name:
            flash('Subcategory name is required', 'error')
            return redirect(url_for('admin.subcategory_new'))
        
        if not category_id:
            flash('Please select a category', 'error')
            return redirect(url_for('admin.subcategory_new'))
        
        slug = slugify(name)
        
        # Check if subcategory exists in this category
        existing = SubCategory.query.filter_by(
            category_id=category_id, 
            slug=slug
        ).first()
        
        if existing:
            flash('A subcategory with this name already exists in this category', 'error')
            return redirect(url_for('admin.subcategory_new'))
        
        subcategory = SubCategory(
            name=name,
            slug=slug,
            description=description,
            category_id=category_id,
            order=order
        )
        
        db.session.add(subcategory)
        db.session.commit()
        
        flash(f'Subcategory "{name}" created successfully!', 'success')
        return redirect(url_for('admin.subcategories'))
    
    return render_template('admin/subcategory_form.html', 
                         subcategory=None, 
                         categories=categories)

@admin_bp.route('/subcategory/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def subcategory_edit(id):
    """Edit existing subcategory"""
    subcategory = SubCategory.query.get_or_404(id)
    categories = Category.query.order_by(Category.name).all()
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        category_id = request.form.get('category_id', type=int)
        order = request.form.get('order', 0, type=int)
        
        if not name:
            flash('Subcategory name is required', 'error')
            return redirect(url_for('admin.subcategory_edit', id=id))
        
        if not category_id:
            flash('Please select a category', 'error')
            return redirect(url_for('admin.subcategory_edit', id=id))
        
        slug = slugify(name)
        
        # Check if subcategory exists (excluding current)
        existing = SubCategory.query.filter_by(
            category_id=category_id, 
            slug=slug
        ).first()
        
        if existing and existing.id != id:
            flash('A subcategory with this name already exists in this category', 'error')
            return redirect(url_for('admin.subcategory_edit', id=id))
        
        subcategory.name = name
        subcategory.slug = slug
        subcategory.description = description
        subcategory.category_id = category_id
        subcategory.order = order
        subcategory.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash(f'Subcategory "{name}" updated successfully!', 'success')
        return redirect(url_for('admin.subcategories'))
    
    return render_template('admin/subcategory_form.html', 
                         subcategory=subcategory, 
                         categories=categories)

@admin_bp.route('/subcategory/<int:id>/delete', methods=['POST'])
@login_required
def subcategory_delete(id):
    """Delete subcategory"""
    subcategory = SubCategory.query.get_or_404(id)
    
    # Check if subcategory has articles
    if subcategory.articles.count() > 0:
        flash(f'Cannot delete subcategory "{subcategory.name}" because it has articles', 'error')
        return redirect(url_for('admin.subcategories'))
    
    name = subcategory.name
    db.session.delete(subcategory)
    db.session.commit()
    
    flash(f'Subcategory "{name}" deleted successfully!', 'success')
    return redirect(url_for('admin.subcategories'))

# ==========================================
# Article Management
# ==========================================

@admin_bp.route('/articles')
@login_required
def articles():
    """List all articles"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    articles = Article.query.order_by(Article.updated_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/articles.html', articles=articles)

@admin_bp.route('/article/new', methods=['GET', 'POST'])
@login_required
def article_new():
    """Create new article"""
    categories = Category.query.order_by(Category.name).all()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        summary = request.form.get('summary', '').strip()
        category_id = request.form.get('category_id', type=int)
        subcategory_id = request.form.get('subcategory_id', type=int) or None
        is_published = request.form.get('is_published') == 'on'
        is_featured = request.form.get('is_featured') == 'on'
        tag_ids = request.form.getlist('tags', type=int)
        
        if not title:
            flash('Article title is required', 'error')
            return redirect(url_for('admin.article_new'))
        
        if not content:
            flash('Article content is required', 'error')
            return redirect(url_for('admin.article_new'))
        
        if not category_id:
            flash('Please select a category', 'error')
            return redirect(url_for('admin.article_new'))
        
        slug = slugify(title)
        
        # Ensure unique slug
        original_slug = slug
        counter = 1
        while Article.query.filter_by(slug=slug).first():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        article = Article(
            title=title,
            slug=slug,
            content=content,
            summary=summary,
            category_id=category_id,
            subcategory_id=subcategory_id,
            is_published=is_published,
            is_featured=is_featured,
            author_id=current_user.id,
            published_at=datetime.utcnow() if is_published else None
        )
        
        # Add tags
        if tag_ids:
            tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            article.tags = tags
        
        article.update_search_vector()
        
        db.session.add(article)
        db.session.commit()
        
        flash(f'Article "{title}" created successfully!', 'success')
        return redirect(url_for('admin.articles'))
    
    all_tags = Tag.query.order_by(Tag.name).all()
    return render_template('admin/article_form.html', 
                         article=None, 
                         categories=categories,
                         all_tags=all_tags)

@admin_bp.route('/article/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def article_edit(id):
    """Edit existing article"""
    article = Article.query.get_or_404(id)
    categories = Category.query.order_by(Category.name).all()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        summary = request.form.get('summary', '').strip()
        category_id = request.form.get('category_id', type=int)
        subcategory_id = request.form.get('subcategory_id', type=int) or None
        is_published = request.form.get('is_published') == 'on'
        is_featured = request.form.get('is_featured') == 'on'
        tag_ids = request.form.getlist('tags', type=int)
        
        if not title:
            flash('Article title is required', 'error')
            return redirect(url_for('admin.article_edit', id=id))
        
        if not content:
            flash('Article content is required', 'error')
            return redirect(url_for('admin.article_edit', id=id))
        
        if not category_id:
            flash('Please select a category', 'error')
            return redirect(url_for('admin.article_edit', id=id))
        
        # Update slug if title changed
        new_slug = slugify(title)
        if new_slug != article.slug:
            # Ensure unique slug
            original_slug = new_slug
            counter = 1
            while Article.query.filter_by(slug=new_slug).filter(Article.id != id).first():
                new_slug = f"{original_slug}-{counter}"
                counter += 1
            article.slug = new_slug
        
        was_published = article.is_published
        
        article.title = title
        article.content = content
        article.summary = summary
        article.category_id = category_id
        article.subcategory_id = subcategory_id
        article.is_published = is_published
        article.is_featured = is_featured
        article.updated_at = datetime.utcnow()
        
        # Update tags
        article.tags = []
        if tag_ids:
            tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            article.tags = tags
        
        # Set published_at if publishing for the first time
        if is_published and not was_published:
            article.published_at = datetime.utcnow()
        
        article.update_search_vector()
        
        db.session.commit()
        
        flash(f'Article "{title}" updated successfully!', 'success')
        return redirect(url_for('admin.articles'))
    
    all_tags = Tag.query.order_by(Tag.name).all()
    return render_template('admin/article_form.html', 
                         article=article, 
                         categories=categories,
                         all_tags=all_tags)

@admin_bp.route('/article/<int:id>/delete', methods=['POST'])
@login_required
def article_delete(id):
    """Delete article"""
    article = Article.query.get_or_404(id)
    
    title = article.title
    db.session.delete(article)
    db.session.commit()
    
    flash(f'Article "{title}" deleted successfully!', 'success')
    return redirect(url_for('admin.articles'))

@admin_bp.route('/api/subcategories/<int:category_id>')
@login_required
def api_subcategories(category_id):
    """API endpoint to get subcategories for a category (for AJAX)"""
    from flask import jsonify
    
    subcategories = SubCategory.query.filter_by(category_id=category_id)\
        .order_by(SubCategory.order, SubCategory.name).all()
    
    return jsonify([
        {'id': sc.id, 'name': sc.name}
        for sc in subcategories
    ])

# ==========================================
# Tag Management
# ==========================================

@admin_bp.route('/tags')
@login_required
def tags():
    """List all tags"""
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('admin/tags.html', tags=tags)

@admin_bp.route('/tag/new', methods=['GET', 'POST'])
@login_required
def tag_new():
    """Create new tag"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        color = request.form.get('color', '#2563eb').strip()
        
        if not name:
            flash('Tag name is required!', 'error')
            return redirect(url_for('admin.tag_new'))
        
        # Check if tag already exists
        existing_tag = Tag.query.filter_by(name=name).first()
        if existing_tag:
            flash(f'Tag "{name}" already exists!', 'error')
            return redirect(url_for('admin.tag_new'))
        
        slug = slugify(name)
        tag = Tag(
            name=name,
            slug=slug,
            description=description,
            color=color
        )
        
        db.session.add(tag)
        db.session.commit()
        
        flash(f'Tag "{name}" created successfully!', 'success')
        return redirect(url_for('admin.tags'))
    
    return render_template('admin/tag_form.html')

@admin_bp.route('/tag/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def tag_edit(id):
    """Edit existing tag"""
    tag = Tag.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        color = request.form.get('color', '#2563eb').strip()
        
        if not name:
            flash('Tag name is required!', 'error')
            return redirect(url_for('admin.tag_edit', id=id))
        
        # Check if name is taken by another tag
        existing_tag = Tag.query.filter(Tag.name == name, Tag.id != id).first()
        if existing_tag:
            flash(f'Tag name "{name}" is already taken!', 'error')
            return redirect(url_for('admin.tag_edit', id=id))
        
        tag.name = name
        tag.slug = slugify(name)
        tag.description = description
        tag.color = color
        
        db.session.commit()
        
        flash(f'Tag "{name}" updated successfully!', 'success')
        return redirect(url_for('admin.tags'))
    
    return render_template('admin/tag_form.html', tag=tag)

@admin_bp.route('/tag/<int:id>/delete', methods=['POST'])
@login_required
def tag_delete(id):
    """Delete tag"""
    tag = Tag.query.get_or_404(id)
    
    name = tag.name
    db.session.delete(tag)
    db.session.commit()
    
    flash(f'Tag "{name}" deleted successfully!', 'success')
    return redirect(url_for('admin.tags'))
