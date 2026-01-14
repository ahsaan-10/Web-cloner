# Quick Start Guide

Get the AI Website Cloner running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- pip package manager
- Internet connection

## Installation (3 steps)

### 1. Install Dependencies

Open terminal (Ctrl + ~) and run:

```bash
pip install streamlit playwright beautifulsoup4 requests
```

### 2. Install Playwright Browsers (Optional)

Only needed if you plan to use the Playwright scraper:

```bash
playwright install
```

### 3. Run the Application

```bash
streamlit run src/app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## First Use

### Clone Your First Website

1. **Enter a URL** in the text box
   - Example: `https://example.com`

2. **Click "CLONE WEBSITE"**
   - Wait for the scraping to complete

3. **Preview the Result**
   - View the cloned HTML code
   - See live preview

4. **Save to Database**
   - Click "SAVE TO CMS DATABASE"
   - Your website is now stored!

### Edit a Cloned Website

1. **Go to "Manage Saved Sites"** in the sidebar

2. **Select a website** from the dropdown

3. **Edit the HTML** in the left panel

4. **See live preview** in the right panel

5. **Save changes** by clicking "Update Website Changes"

## Tips

- Use the default scraper (Requests + BeautifulSoup) for most websites
- Try Playwright scraper if you need JavaScript rendering
- The database is stored in `data/cloned_sites.db`
- All changes are saved automatically to the database

## Troubleshooting

**App won't start?**
- Make sure you're in the Web-cloner directory
- Check if Python and pip are installed: `python --version`

**Scraping fails?**
- Verify the URL starts with `http://` or `https://`
- Check your internet connection
- Some websites block scrapers

**Need help?**
- Check the full README.md
- Review error messages in the terminal

## Next Steps

- Read the full [README.md](README.md) for advanced features
- Explore the code in `src/app.py`
- Check version history in `archive/versions/`

---

Happy cloning!
