"""
Main Application Routes
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app.models import Category, SubCategory, Article
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page - show categories and featured articles"""
    categories = Category.query.order_by(Category.order, Category.name).all()
    featured_articles = Article.query.filter_by(is_published=True, is_featured=True)\
        .order_by(Article.created_at.desc()).limit(6).all()
    recent_articles = Article.query.filter_by(is_published=True)\
        .order_by(Article.created_at.desc()).limit(10).all()
    
    return render_template('index.html', 
                         categories=categories,
                         featured_articles=featured_articles,
                         recent_articles=recent_articles)

@main_bp.route('/health')
def health():
    """Health check endpoint for Docker"""
    return jsonify({'status': 'healthy'}), 200

@main_bp.route('/category/<slug>')
def category(slug):
    """View category and its subcategories"""
    category = Category.query.filter_by(slug=slug).first_or_404()
    subcategories = category.subcategories.order_by(SubCategory.order, SubCategory.name).all()
    articles = category.articles.filter_by(is_published=True)\
        .order_by(Article.created_at.desc()).all()
    
    return render_template('category.html', 
                         category=category,
                         subcategories=subcategories,
                         articles=articles)

@main_bp.route('/category/<category_slug>/<subcategory_slug>')
def subcategory(category_slug, subcategory_slug):
    """View subcategory and its articles"""
    category = Category.query.filter_by(slug=category_slug).first_or_404()
    subcategory = SubCategory.query.filter_by(
        category_id=category.id, 
        slug=subcategory_slug
    ).first_or_404()
    
    articles = subcategory.articles.filter_by(is_published=True)\
        .order_by(Article.created_at.desc()).all()
    
    return render_template('subcategory.html',
                         category=category,
                         subcategory=subcategory,
                         articles=articles)

@main_bp.route('/article/<slug>')
def article(slug):
    """View individual article"""
    article = Article.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # Get related articles from the same subcategory or category
    related_articles = Article.query.filter(
        Article.id != article.id,
        Article.is_published == True
    )
    
    if article.subcategory_id:
        related_articles = related_articles.filter_by(subcategory_id=article.subcategory_id)
    else:
        related_articles = related_articles.filter_by(category_id=article.category_id)
    
    related_articles = related_articles.limit(5).all()
    
    return render_template('article.html', 
                         article=article,
                         related_articles=related_articles)

@main_bp.route('/search')
def search():
    """Search articles"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return render_template('search.html', articles=[], query='')
    
    # Enhanced search using LIKE with multiple conditions
    search_term = f"%{query}%"
    
    # Search in title, content, and summary with weighting
    articles = Article.query.filter(
        Article.is_published == True,
        db.or_(
            Article.title.ilike(search_term),
            Article.content.ilike(search_term),
            Article.summary.ilike(search_term)
        )
    ).order_by(
        # Prioritize title matches
        db.case(
            (Article.title.ilike(search_term), 1),
            else_=2
        ),
        Article.created_at.desc()
    ).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('search.html', 
                         articles=articles,
                         query=query)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/tag/<slug>')
def tag(slug):
    """View articles by tag"""
    from app.models import Tag
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    
    # Get all published articles with this tag
    articles = Article.query.join(Article.tags).filter(
        Tag.id == tag.id,
        Article.is_published == True
    ).order_by(Article.created_at.desc()).all()
    
    return render_template('tag.html', tag=tag, articles=articles)

@main_bp.route('/api/search/suggestions')
def search_suggestions():
    """API endpoint for live search suggestions"""
    from flask import jsonify, url_for
    
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify([])
    
    # Search for matching articles (limit to 8 results)
    search_term = f"%{query}%"
    articles = Article.query.filter(
        Article.is_published == True,
        db.or_(
            Article.title.ilike(search_term),
            Article.summary.ilike(search_term)
        )
    ).order_by(
        # Prioritize title matches
        db.case(
            (Article.title.ilike(search_term), 1),
            else_=2
        ),
        Article.created_at.desc()
    ).limit(8).all()
    
    suggestions = [
        {
            'title': article.title,
            'url': url_for('main.article', slug=article.slug),
            'category': article.category.name,
            'subcategory': article.subcategory.name if article.subcategory else None
        }
        for article in articles
    ]
    
    return jsonify(suggestions)
