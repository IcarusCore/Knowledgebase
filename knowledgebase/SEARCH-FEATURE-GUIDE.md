# Knowledge Base Search Feature Guide

## 🔍 How to Use the Live Search

### Quick Start
1. Click on the search box at the top of any page
2. Start typing (at least 2 characters)
3. Watch as article suggestions appear instantly below
4. Click any suggestion to go directly to that article

### Keyboard Shortcuts (Power User Features!)
|----------------------------|-------------------------------------------|
|          Shortcut 		 |              Action 				 		 |
|----------------------------|-------------------------------------------|
| `Ctrl + K` (Windows/Linux) | Focus the search box from anywhere		 |
| `Cmd + K` (Mac)            | Focus the search box from anywhere		 |
| `↓ Arrow Down`             | Move to the next suggestion               |
| `↑ Arrow Up`               | Move to the previous suggestion           |
| `Enter`                    | Open the currently highlighted suggestion |
| `Escape`                   | Close the suggestions dropdown            |
|----------------------------|-------------------------------------------|

### What the Search Looks For

The search feature searches through:
- ✅ Article **titles** (shown first - highest priority)
- ✅ Article **summaries** (shown after title matches)

### Visual Indicators

**When typing:**
- 🔄 "Searching..." appears with a pulsing animation

**When hovering:**
- 🎨 Suggestion highlights with a blue left border
- 📁 Category/subcategory shown with folder icon

**When using keyboard:**
- ⌨️ Selected item highlights the same as hover
- 📜 Auto-scrolls to keep selected item visible

**When no results:**
- 💭 "No results found" message appears

## 💡 Pro Tips

1. **Fast Navigation**: Press `Ctrl+K` from anywhere on the site to instantly start searching
2. **Keyboard Only**: You can search entirely without touching your mouse!
3. **See Quickly**: Each suggestion shows you which category it belongs to
4. **Smart Search**: The search prioritizes exact title matches over content matches

## 📱 Mobile Usage

On mobile devices:
- Tap the search box to open your keyboard
- Type your search (2+ characters)
- Tap any suggestion to navigate
- Tap outside the dropdown to close it

## 🎯 Search Best Practices

**DO:**
- Use specific keywords from article titles
- Try different word combinations if you don't find what you want
- Use at least 2-3 characters for best results

**DON'T:**
- Type just 1 character (search only starts at 2+ characters)
- Search too quickly - let suggestions load (takes ~300ms)

## 🛠️ Technical Details

**Performance:**
- Debounced search: Waits 300ms after you stop typing before searching
- Shows up to 8 most relevant results
- Searches only published articles
- Results prioritized by: Title match > Summary match > Newest first

**Privacy:**
- All searches happen server-side
- No search data is stored or tracked
- Results based only on published articles

---

## Need Help?

If search isn't working:
1. Make sure you have at least 2 characters typed
2. Check that there are published articles in your knowledge base
3. Try refreshing the page
4. Check browser console for any error messages (F12)

Enjoy your enhanced knowledge base search! 🚀
