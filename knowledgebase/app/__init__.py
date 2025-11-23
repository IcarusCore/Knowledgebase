"""
Knowledge Base Application Package
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register custom template filters
    from app.utils import render_markdown, get_reading_time, truncate_text
    from datetime import datetime
    
    @app.template_filter('markdown')
    def markdown_filter(text):
        return render_markdown(text)
    
    @app.template_filter('reading_time')
    def reading_time_filter(text):
        return get_reading_time(text)
    
    @app.template_filter('truncate')
    def truncate_filter(text, length=200):
        return truncate_text(text, length)
    
    @app.context_processor
    def inject_globals():
        """Inject global variables into all templates"""
        return {
            'current_year': datetime.now().year
        }
    
    # Register blueprints
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp)
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    from app.models import User
    return User.query.get(int(user_id))
