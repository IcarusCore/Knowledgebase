"""
Database Models for Knowledge Base
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

# Association table for many-to-many relationship between articles and tags
article_tags = db.Table('article_tags',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    """Admin user model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """Main category model"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # For future icon support
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subcategories = db.relationship('SubCategory', backref='category', lazy='dynamic', 
                                   cascade='all, delete-orphan')
    articles = db.relationship('Article', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class SubCategory(db.Model):
    """Sub-category model"""
    __tablename__ = 'subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    slug = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    articles = db.relationship('Article', backref='subcategory', lazy='dynamic')
    
    # Ensure unique subcategory names within each category
    __table_args__ = (
        db.UniqueConstraint('category_id', 'name', name='unique_subcategory_per_category'),
        db.UniqueConstraint('category_id', 'slug', name='unique_subcategory_slug_per_category'),
    )
    
    def __repr__(self):
        return f'<SubCategory {self.name}>'


class Article(db.Model):
    """Article/Knowledge base entry model"""
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)  # Short summary for listing pages
    
    # Relationships
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'))
    
    # Status and visibility
    is_published = db.Column(db.Boolean, default=True, index=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    
    # Metadata
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='articles')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime, index=True)
    
    # Search index (for FTS - Full Text Search)
    search_vector = db.Column(db.Text)  # Combined title + content for searching
    
    def __repr__(self):
        return f'<Article {self.title}>'
    
    def update_search_vector(self):
        """Update search vector for full-text search"""
        self.search_vector = f"{self.title} {self.content}"


class Tag(db.Model):
    """Tag model for article categorization and filtering"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200))
    color = db.Column(db.String(7), default='#2563eb')  # Hex color code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with articles
    articles = db.relationship('Article', secondary=article_tags, backref=db.backref('tags', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Tag {self.name}>'
