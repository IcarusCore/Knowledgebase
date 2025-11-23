#!/usr/bin/env python3
"""
Sample Data Generator for Knowledge Base

This script creates sample categories, subcategories, and articles
to help you get started with your knowledge base.

Run with: python sample_data.py
"""
from app import create_app, db
from app.models import User, Category, SubCategory, Article
from datetime import datetime

def create_sample_data():
    """Create sample categories, subcategories, and articles"""
    app = create_app()
    
    with app.app_context():
        # Check if sample data already exists
        if Category.query.count() > 0:
            print("❌ Sample data already exists. Clear your database first if you want to regenerate.")
            return
        
        print("📚 Creating sample knowledge base data...")
        
        # Get or create admin user
        admin = User.query.filter_by(username='Jolleymi800').first()
        if not admin:
            admin = User(username='Jolleymi800')
            admin.set_password('saddlebag-crinkly-deprive')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created")
        
        # Create Categories and Subcategories
        categories_data = {
            "Getting Started": {
                "description": "Everything you need to know to get started",
                "subcategories": ["Installation", "Configuration", "First Steps"],
                "order": 0
            },
            "Documentation": {
                "description": "Comprehensive documentation and guides",
                "subcategories": ["User Guides", "API Reference", "Best Practices"],
                "order": 1
            },
            "Tutorials": {
                "description": "Step-by-step tutorials and how-to guides",
                "subcategories": ["Beginner", "Intermediate", "Advanced"],
                "order": 2
            },
            "FAQ": {
                "description": "Frequently asked questions and answers",
                "subcategories": [],
                "order": 3
            },
            "Troubleshooting": {
                "description": "Common issues and how to resolve them",
                "subcategories": ["Common Errors", "Performance", "Security"],
                "order": 4
            }
        }
        
        categories = {}
        for cat_name, cat_data in categories_data.items():
            category = Category(
                name=cat_name,
                slug=cat_name.lower().replace(' ', '-'),
                description=cat_data["description"],
                order=cat_data["order"]
            )
            db.session.add(category)
            db.session.flush()
            categories[cat_name] = category
            
            # Create subcategories
            for i, subcat_name in enumerate(cat_data["subcategories"]):
                subcategory = SubCategory(
                    name=subcat_name,
                    slug=subcat_name.lower().replace(' ', '-'),
                    category_id=category.id,
                    order=i
                )
                db.session.add(subcategory)
        
        db.session.commit()
        print(f"✓ Created {len(categories_data)} categories")
        
        # Create Sample Articles
        articles_data = [
            {
                "title": "Welcome to the Knowledge Base",
                "category": "Getting Started",
                "subcategory": None,
                "summary": "Learn about this knowledge base and how to use it effectively.",
                "content": """# Welcome!

This is your comprehensive knowledge base. Here you'll find documentation, tutorials, and answers to common questions.

## What You'll Find Here

- **Getting Started** - Everything you need to begin
- **Documentation** - Complete reference materials
- **Tutorials** - Step-by-step guides
- **FAQ** - Quick answers to common questions
- **Troubleshooting** - Solutions to common issues

## Navigation

Use the categories on the home page to browse content, or use the search bar to find specific information quickly.

### Tips for Success

1. Start with the Getting Started category
2. Use the search function for specific topics
3. Check the FAQ for quick answers
4. Bookmark articles you reference often

> Remember: This knowledge base is here to help you succeed!
""",
                "is_featured": True,
                "is_published": True
            },
            {
                "title": "Installation Guide",
                "category": "Getting Started",
                "subcategory": "Installation",
                "summary": "Complete installation instructions for getting set up.",
                "content": """# Installation Guide

Follow these steps to get your system up and running.

## Prerequisites

Before you begin, ensure you have:

- Docker installed (version 20.10 or higher)
- Docker Compose (v2.0+)
- At least 2GB of available RAM
- Internet connection for downloading dependencies

## Installation Steps

### Step 1: Download

```bash
# Clone the repository
git clone https://github.com/yourrepo/knowledgebase.git
cd knowledgebase
```

### Step 2: Configure

Create your configuration file:

```bash
cp config.example.py config.py
# Edit config.py with your settings
```

### Step 3: Deploy

```bash
# Build and start the containers
docker compose up -d
```

### Step 4: Verify

Check that everything is running:

```bash
docker compose ps
```

You should see all services running with status "Up".

## Next Steps

- Log in to the admin panel
- Create your first category
- Start adding content

---

Need help? Check out the Configuration guide or visit our Troubleshooting section.
""",
                "is_featured": False,
                "is_published": True
            },
            {
                "title": "Markdown Formatting Guide",
                "category": "Documentation",
                "subcategory": "User Guides",
                "summary": "Learn how to format your articles using Markdown.",
                "content": """# Markdown Formatting Guide

Articles in this knowledge base support Markdown formatting for rich content.

## Basic Formatting

### Headings

```markdown
# Heading 1
## Heading 2
### Heading 3
```

### Text Styling

**Bold text** - `**bold**` or `__bold__`
*Italic text* - `*italic*` or `_italic_`
~~Strikethrough~~ - `~~strikethrough~~`

### Lists

Unordered lists:
- Item 1
- Item 2
  - Nested item
  - Another nested item

Ordered lists:
1. First item
2. Second item
3. Third item

### Links and Images

[Link text](https://example.com)

![Image alt text](image-url.jpg)

### Code

Inline code: `code here`

Code blocks:

```python
def hello_world():
    print("Hello, World!")
```

### Blockquotes

> This is a blockquote.
> It can span multiple lines.

### Tables

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

## Advanced Features

### Horizontal Rule

---

### Task Lists

- [x] Completed task
- [ ] Incomplete task

## Best Practices

1. Use headings to structure your content
2. Add code blocks for technical content
3. Use tables for structured data
4. Include images when helpful
5. Keep paragraphs concise

Happy writing! 📝
""",
                "is_featured": True,
                "is_published": True
            },
            {
                "title": "How to Search Effectively",
                "category": "Tutorials",
                "subcategory": "Beginner",
                "summary": "Tips and tricks for finding information quickly.",
                "content": """# How to Search Effectively

Master the search function to find information quickly.

## Search Tips

### Be Specific

Instead of: *"docker"*
Try: *"docker compose setup"*

### Use Keywords

Think about the key terms that would appear in the article you're looking for.

### Try Different Terms

If you don't find what you need, try synonyms or related terms.

## Search Shortcuts

Press `Ctrl+K` (or `Cmd+K` on Mac) to quickly access the search bar from anywhere.

## Understanding Results

Search results show:
- Article title
- Category and subcategory
- Publication date
- Summary or excerpt

Results are sorted with title matches first, followed by content matches.

## Still Can't Find It?

- Browse categories manually
- Check the FAQ section
- Contact an administrator for help

Happy searching! 🔍
""",
                "is_featured": False,
                "is_published": True
            },
            {
                "title": "Common Installation Issues",
                "category": "Troubleshooting",
                "subcategory": "Common Errors",
                "summary": "Solutions to frequently encountered installation problems.",
                "content": """# Common Installation Issues

Quick solutions to common problems during installation.

## Port Already in Use

**Error**: `Bind for 0.0.0.0:8888 failed: port is already allocated`

**Solution**:
1. Check what's using the port: `sudo lsof -i :8888`
2. Stop the conflicting service
3. Or change the port in `docker-compose.yml`

## Database Connection Failed

**Error**: `OperationalError: unable to open database file`

**Solution**:
- Ensure the `/app/instance` directory exists
- Check file permissions
- Verify the volume is properly mounted

## Docker Daemon Not Running

**Error**: `Cannot connect to the Docker daemon`

**Solution**:
```bash
# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker
```

## Out of Memory

**Error**: Container exits with code 137

**Solution**:
- Increase Docker's memory allocation
- Check system resources with `docker stats`
- Reduce number of running containers

## Still Having Issues?

If these solutions don't help:
1. Check Docker logs: `docker compose logs`
2. Review the Installation Guide
3. Contact support with error details

---

*Last updated: November 2024*
""",
                "is_featured": False,
                "is_published": True
            }
        ]
        
        # Create articles
        for article_data in articles_data:
            category = categories[article_data["category"]]
            subcategory = None
            
            if article_data["subcategory"]:
                subcategory = SubCategory.query.filter_by(
                    category_id=category.id,
                    name=article_data["subcategory"]
                ).first()
            
            article = Article(
                title=article_data["title"],
                slug=article_data["title"].lower().replace(' ', '-').replace(':', ''),
                content=article_data["content"],
                summary=article_data["summary"],
                category_id=category.id,
                subcategory_id=subcategory.id if subcategory else None,
                is_published=article_data["is_published"],
                is_featured=article_data["is_featured"],
                author_id=admin.id,
                published_at=datetime.utcnow()
            )
            article.update_search_vector()
            db.session.add(article)
        
        db.session.commit()
        print(f"✓ Created {len(articles_data)} sample articles")
        
        print("\n🎉 Sample data created successfully!")
        print(f"\nYou now have:")
        print(f"  - {Category.query.count()} categories")
        print(f"  - {SubCategory.query.count()} subcategories")
        print(f"  - {Article.query.count()} articles")
        print(f"\nVisit http://localhost:8888 to see your knowledge base!")

if __name__ == '__main__':
    create_sample_data()
