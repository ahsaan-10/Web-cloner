# AI Website Cloner & CMS

A powerful web scraping tool with an integrated Content Management System (CMS) built with Streamlit. Clone any website, save it to a database, and edit the content through an intuitive admin panel.

## Features

- **Website Cloning**: Clone any website using advanced scraping techniques
- **Dual Scraping Methods**:
  - BeautifulSoup + Requests (fast, reliable)
  - Playwright (for JavaScript-heavy sites)
- **Database Integration**: SQLite database for storing cloned websites
- **Admin Panel**: Manage and edit saved websites
- **Live Editor**: Real-time HTML editing with live preview
- **Security Fixes**: Automatic removal of CSP headers and integrity checks
- **URL Normalization**: Converts relative URLs to absolute URLs

## Project Structure

```
Web-cloner/
├── src/
│   ├── app.py                          # Main Streamlit application
│   ├── scrapers/
│   │   └── playwright_scraper.py       # Alternative Playwright scraper
│   └── database/
│       └── (database modules)
├── data/
│   └── cloned_sites.db                 # Active database
├── archive/
│   ├── versions/                       # Previous code versions
│   │   ├── app_v1.txt
│   │   ├── app_v2.txt
│   │   └── app_v3.txt
│   └── old_databases/                  # Old database files
├── docs/
│   ├── version_notes.txt              # Version history notes
│   └── installation_notes.txt         # Installation instructions
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git ignore rules
└── README.md                          # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Web-cloner
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers** (if using Playwright scraper)
   ```bash
   playwright install
   ```

## Usage

### Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run src/app.py
   ```

2. **Access the application**
   - Open your browser and navigate to: `http://localhost:8501`

### Using the Web Cloner

#### Clone a New Website

1. Navigate to "Clone New Site" in the sidebar
2. Enter the target website URL (e.g., `https://example.com`)
3. Click "CLONE WEBSITE"
4. Preview the cloned content
5. Click "SAVE TO CMS DATABASE" to store it

#### Manage Saved Websites

1. Navigate to "Manage Saved Sites" in the sidebar
2. Select a website from the dropdown
3. Edit the HTML code in the editor
4. See live preview on the right
5. Click "Update Website Changes" to save

## Features Breakdown

### Scraping Engine

The application uses a sophisticated scraping system:

- **User-Agent Spoofing**: Mimics real browser requests
- **Encoding Fix**: Forces UTF-8 encoding to prevent gibberish
- **Security Cleanup**: Removes CSP headers and integrity checks
- **Link Fixing**: Converts relative URLs to absolute
- **Base Tag Injection**: Opens links in new tabs

### Database Schema

```sql
CREATE TABLE websites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    html_content TEXT,
    created_at TEXT
);
```

### Admin Panel

- **Direct Access**: No login required (can be extended)
- **Two-Panel Layout**: Editor and live preview side-by-side
- **Real-time Updates**: Changes reflect immediately
- **Site Management**: View, edit, and manage all cloned sites

## Technical Details

### Technologies Used

- **Streamlit**: Web framework for the UI
- **Requests**: HTTP library for web scraping
- **BeautifulSoup4**: HTML parsing and manipulation
- **Playwright**: Browser automation for JavaScript sites
- **SQLite3**: Local database storage

### Scraping Methods

1. **Requests + BeautifulSoup** (Default)
   - Faster and lighter
   - Works for most static websites
   - Lower resource consumption

2. **Playwright** (Alternative)
   - Handles JavaScript-rendered content
   - Better for SPAs and dynamic sites
   - Higher resource consumption

## Configuration

### Customization Options

Edit `src/app.py` to customize:

- **Database location**: Change `cloned_sites.db` path (line 16)
- **Timeout settings**: Adjust request timeout (line 82)
- **UI theme**: Modify CSS in the markdown section (lines 115-157)
- **Page config**: Change title, icon, layout (lines 108-113)

## Development

### Version History

- **v1**: Initial UI design (no functionality)
- **v2**: Basic Playwright scraper integration
- **v3**: Added Requests scraper with download feature
- **Current**: Full CMS with database and admin panel

All previous versions are archived in `archive/versions/`

### Database Migration

Old databases have been moved to `archive/old_databases/`:
- `admin_panel.db`
- `cms_core.db`
- `cms_database.db`

Active database: `data/cloned_sites.db`

## Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

2. **Playwright not working**
   - Run: `playwright install`
   - Check if browsers are installed

3. **Database locked**
   - Close other connections to the database
   - Restart the application

4. **Scraping fails**
   - Check if the website blocks bots
   - Try the Playwright method for JavaScript sites
   - Verify internet connection

### Getting Help

Open the terminal with `Ctrl + ~` and check error messages.

## Future Enhancements

- [ ] User authentication system
- [ ] Multi-user support
- [ ] Export to different formats (PDF, DOCX)
- [ ] Scheduled scraping
- [ ] Diff viewer for tracking changes
- [ ] Proxy support
- [ ] Rate limiting
- [ ] API integration

## License

Final Year Project - 2025

## Contributing

This is a final year project. Contributions and suggestions are welcome.

## Acknowledgments

- Built with Streamlit
- Scraping powered by BeautifulSoup and Playwright
- Database management with SQLite

---

**Note**: This tool is intended for educational purposes only. Always respect website terms of service and robots.txt when scraping.
