# 🚀 Knowledge Base - Complete Deployment Guide

## What You Have

A fully-featured Knowledge Base application with:
- ✅ Category & Subcategory organization
- ✅ Article management with Markdown support
- ✅ Full-text search with live suggestions
- ✅ Tag system for cross-category organization
- ✅ Admin panel with complete CRUD operations
- ✅ Beautiful blue dark theme
- ✅ Mobile-responsive design
- ✅ User authentication
- ✅ Article drafts and featured articles

## Quick Start

### 1. Extract the Project

```bash
tar -xzf knowledgebase-COMPLETE-FINAL.tar.gz
cd knowledgebase
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Database Migration

**Choose ONE method:**

**Option A: Flask-Migrate (Recommended)**
```bash
flask db init
flask db migrate -m "Initial migration with tags"
flask db upgrade
```

**Option B: Python Shell**
```python
python3
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
...     print("Database created!")
```

**Option C: Manual SQL**
See `DATABASE-MIGRATION-TAGS.md` for SQL scripts

### 4. Create Admin User

```bash
python3
```

```python
from app import app, db
from app.models import User

with app.app_context():
    admin = User(username='admin')
    admin.set_password('your-secure-password')  # Change this!
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
```

### 5. (Optional) Add Sample Data

```bash
python3 sample_data.py
```

This creates:
- Categories
- Subcategories
- Sample articles
- Sample tags

### 6. Run the Application

**Development:**
```bash
python3 run.py
```

**Production (with Gunicorn):**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

**Access the site:**
- Public: http://localhost:5000
- Admin Login: http://localhost:5000/auth/login

## Configuration

### Environment Variables

Create a `.env` file:

```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=production  # Use 'development' for dev
SECRET_KEY=your-very-secret-key-here-change-this

# Database (SQLite default)
DATABASE_URL=sqlite:///knowledge_base.db

# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/knowledgebase

# For MySQL:
# DATABASE_URL=mysql://user:password@localhost/knowledgebase
```

### Security Settings

**Important:** Change these in `config.py`:

```python
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-random-secret-key'
```

Generate a secure secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Using the Application

### Admin Workflow

1. **Login**
   - Navigate to `/auth/login`
   - Enter admin credentials

2. **Create Categories**
   - Go to Admin Dashboard → Categories
   - Click "+ New Category"
   - Fill in name, description, order
   - Save

3. **Create Subcategories** (Optional)
   - Go to Subcategories
   - Select parent category
   - Create subcategory

4. **Create Tags**
   - Go to Tags
   - Click "+ New Tag"
   - Choose name, description, color
   - Save

5. **Create Articles**
   - Click "+ New Article"
   - Write content in Markdown
   - Select category, subcategory
   - Assign tags
   - Choose Published/Featured
   - Save

### Public Features

1. **Browse Articles**
   - Homepage shows featured articles
   - Navigate by category/subcategory
   - Use search with autocomplete

2. **Search**
   - Type in search box (2+ chars)
   - View instant suggestions
   - Use keyboard navigation (arrows, Enter)
   - Press Ctrl+K to focus search

3. **Filter by Tags**
   - Click any tag on an article
   - View all articles with that tag
   - Navigate between related content

## Docker Deployment

### Build Image

```bash
docker build -t knowledgebase .
```

### Run Container

```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  --name knowledgebase \
  knowledgebase
```

### Using Docker Compose

```bash
docker-compose up -d
```

## Production Deployment

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/knowledgebase/app/static;
        expires 30d;
    }
}
```

### Systemd Service

Create `/etc/systemd/system/knowledgebase.service`:

```ini
[Unit]
Description=Knowledge Base Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/knowledgebase
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable knowledgebase
sudo systemctl start knowledgebase
```

## Backup Strategy

### Database Backup

**SQLite:**
```bash
cp knowledge_base.db knowledge_base.db.backup
```

**PostgreSQL:**
```bash
pg_dump knowledgebase > backup.sql
```

**MySQL:**
```bash
mysqldump knowledgebase > backup.sql
```

### Full Backup

```bash
tar -czf kb-backup-$(date +%Y%m%d).tar.gz \
  knowledge_base.db \
  app/static/uploads \
  config.py
```

## Maintenance

### Update Application

```bash
git pull  # If using git
pip install -r requirements.txt --upgrade
flask db upgrade  # If schema changed
sudo systemctl restart knowledgebase
```

### Monitor Logs

```bash
# Systemd service
sudo journalctl -u knowledgebase -f

# Docker
docker logs -f knowledgebase

# Direct
tail -f logs/app.log
```

## Troubleshooting

### Database Issues

**Problem:** "Table doesn't exist"
**Solution:** Run `db.create_all()` or migration

**Problem:** "Foreign key constraint"
**Solution:** Check relationship definitions in models.py

### Performance Issues

**Problem:** Slow search
**Solution:** 
- Add database indexes
- Use full-text search extensions
- Cache common queries

**Problem:** Slow page loads
**Solution:**
- Enable pagination
- Optimize images
- Use CDN for static files

### Authentication Issues

**Problem:** Can't login
**Solution:**
- Reset admin password via Python shell
- Check SECRET_KEY is set
- Verify database connection

## Customization

### Change Theme Colors

Edit `/app/static/css/style.css`:

```css
:root {
    --primary-bg: #your-color;
    --accent-blue: #your-accent;
    /* ... other colors */
}
```

### Add Custom Markdown Extensions

Edit `app/utils.py`:

```python
def render_markdown(text):
    extensions = [
        'fenced_code',
        'tables',
        'nl2br',
        'your-extension'  # Add here
    ]
    return markdown(text, extensions=extensions)
```

### Modify Navigation

Edit `/app/templates/base.html`:

```html
<div class="nav-menu">
    <a href="/" class="nav-link">Home</a>
    <!-- Add your links here -->
</div>
```

## Features Overview

### Search Features
- Live autocomplete suggestions
- Keyboard navigation (↑↓ arrows, Enter)
- Search in titles and summaries
- Ctrl+K shortcut
- Debounced requests (300ms)

### Tag Features
- Color-coded badges
- Many-to-many relationships
- Click to filter articles
- Cross-category organization
- Visual selection in admin

### Admin Features
- Complete CRUD operations
- Markdown editor with toolbar
- Category management
- Tag management
- User-friendly forms
- Empty states

### Security Features
- Password hashing (Werkzeug)
- Login required decorators
- CSRF protection
- Session management
- SQL injection prevention (SQLAlchemy)

## Support

### File Structure
```
knowledgebase/
├── app/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── routes.py          # Public routes
│   ├── admin.py           # Admin routes
│   ├── auth.py            # Authentication
│   ├── utils.py           # Helper functions
│   ├── static/            # CSS, JS, images
│   └── templates/         # HTML templates
├── config.py              # Configuration
├── run.py                 # Application entry
├── requirements.txt       # Dependencies
├── Dockerfile            # Docker config
└── docker-compose.yml    # Docker Compose

```

### Key Files
- **models.py**: Database schema
- **routes.py**: Public pages
- **admin.py**: Admin panel
- **base.html**: Site template
- **style.css**: Main stylesheet

## Getting Help

1. Check logs for errors
2. Verify database connection
3. Ensure all dependencies installed
4. Review configuration settings
5. Test in development mode first

---

## 🎉 You're Ready!

Your Knowledge Base is production-ready with all features working:
- Search with autocomplete
- Tags for organization
- Beautiful UI
- Mobile-responsive
- Secure admin panel
- Complete documentation

**Start building your knowledge base today!** 📚
