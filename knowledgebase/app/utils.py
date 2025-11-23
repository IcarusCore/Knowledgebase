"""
Utility functions for the Knowledge Base
"""
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown.extensions.nl2br import Nl2BrExtension
import bleach
from pygments.formatters import HtmlFormatter

# Allowed HTML tags for sanitization
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote', 'code', 'pre', 'hr', 'div', 'span',
    'ul', 'ol', 'li', 'dl', 'dt', 'dd',
    'a', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'sup', 'sub', 'abbr',
]

ALLOWED_ATTRIBUTES = {
    '*': ['class', 'id'],
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'code': ['class'],
    'pre': ['class'],
    'div': ['class'],
    'span': ['class'],
}

def render_markdown(text):
    """
    Convert markdown text to HTML with syntax highlighting
    
    Args:
        text: Markdown formatted text
        
    Returns:
        Safe HTML string
    """
    if not text:
        return ''
    
    # Configure markdown with extensions
    md = markdown.Markdown(
        extensions=[
            FencedCodeExtension(),
            CodeHiliteExtension(
                css_class='highlight',
                linenums=False,
                guess_lang=True
            ),
            TableExtension(),
            TocExtension(
                permalink=True,
                permalink_title='Link to this section'
            ),
            Nl2BrExtension(),
            'extra',  # Includes several useful extensions
        ],
        output_format='html5'
    )
    
    # Convert markdown to HTML
    html = md.convert(text)
    
    # Sanitize the HTML to prevent XSS
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    
    return clean_html

def get_pygments_css():
    """
    Get CSS for Pygments syntax highlighting
    
    Returns:
        CSS string for syntax highlighting
    """
    formatter = HtmlFormatter(style='monokai')
    return formatter.get_style_defs('.highlight')

def truncate_text(text, max_length=200, suffix='...'):
    """
    Truncate text to a maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length].rsplit(' ', 1)[0] + suffix

def highlight_search_term(text, query, max_length=300):
    """
    Highlight search term in text and return a snippet
    
    Args:
        text: Text to search in
        query: Search query
        max_length: Maximum length of snippet
        
    Returns:
        Text snippet with search term context
    """
    if not text or not query:
        return truncate_text(text, max_length)
    
    text_lower = text.lower()
    query_lower = query.lower()
    
    # Find the position of the query
    pos = text_lower.find(query_lower)
    
    if pos == -1:
        # Query not found, return beginning
        return truncate_text(text, max_length)
    
    # Calculate snippet range
    start = max(0, pos - max_length // 3)
    end = min(len(text), pos + len(query) + max_length * 2 // 3)
    
    snippet = text[start:end]
    
    # Add ellipsis if truncated
    if start > 0:
        snippet = '...' + snippet
    if end < len(text):
        snippet = snippet + '...'
    
    return snippet

def get_reading_time(text):
    """
    Calculate estimated reading time for text
    
    Args:
        text: Text content
        
    Returns:
        Estimated reading time in minutes
    """
    if not text:
        return 0
    
    # Average reading speed: 200-250 words per minute
    words = len(text.split())
    minutes = max(1, round(words / 225))
    
    return minutes
