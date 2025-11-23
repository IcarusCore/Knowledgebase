# Database Migration: Tags System

## Overview
This migration adds the Tags feature to your Knowledge Base, including:
- `tags` table for tag storage
- `article_tags` association table for many-to-many relationships

## Migration Steps

### Option 1: Automatic Migration (Recommended)

If you're using Flask-Migrate:

```bash
# Initialize migrations (if not already done)
flask db init

# Create migration
flask db migrate -m "Add tags system"

# Apply migration
flask db upgrade
```

### Option 2: Manual SQL (If not using Flask-Migrate)

Run the following SQL commands in your database:

#### For SQLite:

```sql
-- Create tags table
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200),
    color VARCHAR(7) DEFAULT '#2563eb',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create article_tags association table
CREATE TABLE article_tags (
    article_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (article_id, tag_id),
    FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_tags_name ON tags(name);
CREATE INDEX idx_tags_slug ON tags(slug);
CREATE INDEX idx_article_tags_article ON article_tags(article_id);
CREATE INDEX idx_article_tags_tag ON article_tags(tag_id);
```

#### For PostgreSQL:

```sql
-- Create tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200),
    color VARCHAR(7) DEFAULT '#2563eb',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create article_tags association table
CREATE TABLE article_tags (
    article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (article_id, tag_id)
);

-- Create indexes for better performance
CREATE INDEX idx_tags_name ON tags(name);
CREATE INDEX idx_tags_slug ON tags(slug);
CREATE INDEX idx_article_tags_article ON article_tags(article_id);
CREATE INDEX idx_article_tags_tag ON article_tags(tag_id);
```

#### For MySQL/MariaDB:

```sql
-- Create tags table
CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(200),
    color VARCHAR(7) DEFAULT '#2563eb',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tags_name (name),
    INDEX idx_tags_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create article_tags association table
CREATE TABLE article_tags (
    article_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (article_id, tag_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    INDEX idx_article_tags_article (article_id),
    INDEX idx_article_tags_tag (tag_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Option 3: Using Python Shell

You can also create the tables using Python:

```python
# In your terminal/command prompt:
python3

# Then in the Python shell:
from app import app, db
with app.app_context():
    db.create_all()
    print("Tables created successfully!")
```

## Verification

After migration, verify the tables were created:

### SQLite:
```bash
sqlite3 your_database.db
.tables
# You should see 'tags' and 'article_tags' in the list
.schema tags
.schema article_tags
```

### PostgreSQL:
```sql
\dt
# You should see 'tags' and 'article_tags' in the list
\d tags
\d article_tags
```

### MySQL:
```sql
SHOW TABLES;
# You should see 'tags' and 'article_tags' in the list
DESCRIBE tags;
DESCRIBE article_tags;
```

## Sample Data (Optional)

If you want to add some initial tags:

```sql
INSERT INTO tags (name, slug, description, color) VALUES
    ('Python', 'python', 'Python programming language', '#3776ab'),
    ('Tutorial', 'tutorial', 'Step-by-step guides', '#10b981'),
    ('API', 'api', 'API documentation and guides', '#f59e0b'),
    ('Security', 'security', 'Security best practices', '#ef4444'),
    ('Database', 'database', 'Database related content', '#8b5cf6'),
    ('Best Practices', 'best-practices', 'Recommended approaches', '#06b6d4');
```

## Rollback (If Needed)

If you need to rollback the migration:

### Flask-Migrate:
```bash
flask db downgrade
```

### Manual SQL:
```sql
DROP TABLE IF EXISTS article_tags;
DROP TABLE IF EXISTS tags;
```

## Testing

After migration, test the tags feature:

1. Log in to admin panel
2. Navigate to "Tags" from the dashboard
3. Create a new tag
4. Edit an article and assign tags
5. View the article to see tags displayed
6. Click a tag to view all articles with that tag

## Troubleshooting

**Problem:** "Table already exists" error
**Solution:** Drop the existing tables first (backup your data!)

**Problem:** Foreign key constraint errors
**Solution:** Ensure the articles table exists before creating article_tags

**Problem:** Migration not detected
**Solution:** Make sure all model changes are saved and Flask-Migrate can import the models

## Support

If you encounter issues:
1. Check your database connection
2. Verify all dependencies are installed
3. Ensure your models.py is updated with Tag model
4. Check database user permissions

---

**Migration Complete!** ✅

Your Knowledge Base now supports tags for better organization and searchability!
