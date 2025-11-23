/**
 * Knowledge Base - Main JavaScript
 */

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            flash.style.transform = 'translateX(100%)';
            setTimeout(function() {
                flash.remove();
            }, 300);
        }, 5000);
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Search input focus shortcut (Ctrl/Cmd + K)
    document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('navSearchInput');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Close search suggestions on Escape
        if (e.key === 'Escape') {
            const suggestions = document.getElementById('searchSuggestions');
            if (suggestions) {
                suggestions.classList.remove('active');
            }
        }
    });
    
    // Live search suggestions
    initLiveSearch();
});

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });
    
    return isValid;
}

// Live search functionality
function initLiveSearch() {
    const searchInput = document.getElementById('navSearchInput');
    const suggestionsDiv = document.getElementById('searchSuggestions');
    
    if (!searchInput || !suggestionsDiv) return;
    
    let searchTimeout;
    let lastQuery = '';
    let selectedIndex = -1;
    
    // Handle input changes
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.trim();
        
        // Clear previous timeout
        clearTimeout(searchTimeout);
        
        // Reset selection
        selectedIndex = -1;
        
        // If query is too short, hide suggestions
        if (query.length < 2) {
            suggestionsDiv.classList.remove('active');
            return;
        }
        
        // Avoid duplicate searches
        if (query === lastQuery) return;
        
        // Debounce search requests
        searchTimeout = setTimeout(() => {
            fetchSearchSuggestions(query);
            lastQuery = query;
        }, 300);
    });
    
    // Handle keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        const items = suggestionsDiv.querySelectorAll('.search-suggestion-item');
        
        if (items.length === 0) return;
        
        // Arrow Down
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            selectedIndex = (selectedIndex + 1) % items.length;
            updateSelectedItem(items, selectedIndex);
        }
        // Arrow Up
        else if (e.key === 'ArrowUp') {
            e.preventDefault();
            selectedIndex = selectedIndex <= 0 ? items.length - 1 : selectedIndex - 1;
            updateSelectedItem(items, selectedIndex);
        }
        // Enter
        else if (e.key === 'Enter' && selectedIndex >= 0) {
            e.preventDefault();
            items[selectedIndex].click();
        }
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsDiv.contains(e.target)) {
            suggestionsDiv.classList.remove('active');
            selectedIndex = -1;
        }
    });
    
    // Show suggestions when focusing on input with existing query
    searchInput.addEventListener('focus', function() {
        if (searchInput.value.trim().length >= 2 && suggestionsDiv.children.length > 0) {
            suggestionsDiv.classList.add('active');
        }
    });
}

// Update selected suggestion item
function updateSelectedItem(items, index) {
    items.forEach((item, i) => {
        if (i === index) {
            item.classList.add('selected');
            item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        } else {
            item.classList.remove('selected');
        }
    });
}

// Fetch search suggestions from API
function fetchSearchSuggestions(query) {
    const suggestionsDiv = document.getElementById('searchSuggestions');
    
    // Show loading state
    suggestionsDiv.innerHTML = '<div class="search-suggestion-loading">Searching...</div>';
    suggestionsDiv.classList.add('active');
    
    fetch(`/api/search/suggestions?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(suggestions => {
            displaySearchSuggestions(suggestions);
        })
        .catch(error => {
            console.error('Error fetching search suggestions:', error);
            suggestionsDiv.innerHTML = '<div class="search-suggestion-empty">Error loading results</div>';
        });
}

// Display search suggestions in dropdown
function displaySearchSuggestions(suggestions) {
    const suggestionsDiv = document.getElementById('searchSuggestions');
    
    // Clear previous suggestions
    suggestionsDiv.innerHTML = '';
    
    if (suggestions.length === 0) {
        suggestionsDiv.innerHTML = '<div class="search-suggestion-empty">No results found</div>';
        suggestionsDiv.classList.add('active');
        return;
    }
    
    // Create suggestion items
    suggestions.forEach(suggestion => {
        const item = document.createElement('a');
        item.href = suggestion.url;
        item.className = 'search-suggestion-item';
        
        let metaText = suggestion.category;
        if (suggestion.subcategory) {
            metaText += ` / ${suggestion.subcategory}`;
        }
        
        item.innerHTML = `
            <div class="search-suggestion-title">${escapeHtml(suggestion.title)}</div>
            <div class="search-suggestion-meta">${escapeHtml(metaText)}</div>
        `;
        
        suggestionsDiv.appendChild(item);
    });
    
    suggestionsDiv.classList.add('active');
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
