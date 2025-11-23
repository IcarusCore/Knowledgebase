#!/usr/bin/env python3
"""
Knowledge Base Application Entry Point
"""
from app import create_app, db
from app.models import User, Category, SubCategory, Article

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Category': Category,
        'SubCategory': SubCategory,
        'Article': Article
    }

@app.cli.command()
def init_db():
    """Initialize the database and create admin user"""
    db.create_all()
    
    # Check if admin user exists
    admin = User.query.filter_by(username='Jolleymi800').first()
    if not admin:
        admin = User(username='Jolleymi800')
        admin.set_password('saddlebag-crinkly-deprive')
        db.session.add(admin)
        db.session.commit()
        print('✓ Admin user created successfully')
    else:
        print('✓ Admin user already exists')
    
    print('✓ Database initialized successfully')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Auto-create admin user if it doesn't exist
        admin = User.query.filter_by(username='Jolleymi800').first()
        if not admin:
            admin = User(username='Jolleymi800')
            admin.set_password('saddlebag-crinkly-deprive')
            db.session.add(admin)
            db.session.commit()
            print('✓ Admin user created')
    
    app.run(host='0.0.0.0', port=8888, debug=False)
