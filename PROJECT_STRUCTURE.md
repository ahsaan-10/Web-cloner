# Project Structure Documentation

Detailed documentation of the Web Cloner project structure and file organization.

## Directory Tree

```
Web-cloner/
├── src/                                # Source code directory
│   ├── __init__.py                    # Package initialization
│   ├── app.py                         # Main Streamlit application
│   ├── scrapers/                      # Web scraping modules
│   │   ├── __init__.py               # Scrapers package init
│   │   └── playwright_scraper.py     # Playwright-based scraper
│   └── database/                      # Database management
│       └── __init__.py               # Database package init
│
├── data/                              # Active data storage
│   └── cloned_sites.db               # Main SQLite database
│
├── archive/                           # Historical files
│   ├── versions/                     # Previous code versions
│   │   ├── app_v1.txt               # Version 1: UI only
│   │   ├── app_v2.txt               # Version 2: Playwright scraper
│   │   └── app_v3.txt               # Version 3: Dual scrapers
│   └── old_databases/                # Deprecated databases
│       ├── admin_panel.db           # Old admin database
│       ├── cms_core.db              # Old core database
│       └── cms_database.db          # Old CMS database
│
├── docs/                              # Documentation files
│   ├── version_notes.txt            # Version history notes
│   └── installation_notes.txt       # Installation guide
│
├── .git/                              # Git repository data
│
├── .gitignore                         # Git ignore rules
├── README.md                          # Main project documentation
├── QUICKSTART.md                      # Quick start guide
├── CHANGELOG.md                       # Version history
├── PROJECT_STRUCTURE.md               # This file
└── requirements.txt                   # Python dependencies
```

## File Descriptions

### Root Level Files

#### README.md
- **Purpose**: Main project documentation
- **Contains**:
  - Project overview
  - Installation instructions
  - Usage guide
  - Feature descriptions
  - Troubleshooting tips

#### QUICKSTART.md
- **Purpose**: Fast setup guide
- **Contains**:
  - Quick installation steps
  - First-use tutorial
  - Common tips
  - Basic troubleshooting

#### CHANGELOG.md
- **Purpose**: Version history
- **Contains**:
  - All version changes
  - Feature additions
  - Bug fixes
  - Migration notes

#### PROJECT_STRUCTURE.md
- **Purpose**: This file - structure documentation
- **Contains**:
  - Directory tree
  - File descriptions
  - Organizational logic

#### requirements.txt
- **Purpose**: Python dependencies
- **Contains**:
  - Required packages
  - Version specifications
  - Comments for clarity

#### .gitignore
- **Purpose**: Git exclusion rules
- **Contains**:
  - Python artifacts to ignore
  - IDE files to ignore
  - Database ignore options
  - Temporary files

### Source Code (`src/`)

#### src/app.py
- **Purpose**: Main application entry point
- **Size**: ~244 lines
- **Contains**:
  - Database setup functions
  - Web scraping logic
  - Streamlit UI configuration
  - Admin panel implementation
  - CMS editor interface

**Key Functions**:
- `init_db()`: Initialize database
- `save_site_to_db()`: Save cloned website
- `get_all_sites()`: Retrieve all saved sites
- `get_html_by_id()`: Get specific site HTML
- `update_html_in_db()`: Update site content
- `scrape_website()`: Main scraping function

**Features**:
- Two-tab interface: Clone | Manage
- Live HTML editor
- Real-time preview
- Database persistence

#### src/scrapers/playwright_scraper.py
- **Purpose**: Alternative scraping method
- **Size**: ~320 lines
- **Contains**:
  - Playwright-based scraper
  - Browser automation
  - Error handling
  - UI components

**Key Functions**:
- `scrape_website()`: Playwright scraping implementation

**Features**:
- Headless browser automation
- JavaScript rendering
- SSL error handling
- Timeout management

#### src/__init__.py
- **Purpose**: Package initialization
- **Contains**:
  - Version info
  - Author info
  - Package metadata

#### src/scrapers/__init__.py
- **Purpose**: Scrapers package initialization
- **Contains**:
  - Module imports
  - Exposed functions

#### src/database/__init__.py
- **Purpose**: Database package initialization
- **Contains**:
  - Future database modules
  - Currently a placeholder

### Data Directory (`data/`)

#### data/cloned_sites.db
- **Purpose**: Active SQLite database
- **Schema**:
  ```sql
  CREATE TABLE websites (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      url TEXT,
      html_content TEXT,
      created_at TEXT
  );
  ```
- **Size**: Variable (grows with cloned sites)
- **Location**: Separated from code for clarity

### Archive Directory (`archive/`)

#### archive/versions/app_v1.txt
- **Version**: 0.1.0
- **Purpose**: First version - UI design only
- **Features**:
  - Streamlit setup
  - CSS styling
  - No scraping functionality

#### archive/versions/app_v2.txt
- **Version**: 0.2.0
- **Purpose**: Added Playwright scraper
- **Features**:
  - Browser automation
  - Full HTML extraction
  - Basic scraping

#### archive/versions/app_v3.txt
- **Version**: 0.3.0
- **Purpose**: Dual scraper approach
- **Features**:
  - Requests + Playwright
  - Download functionality
  - Method selection

#### archive/old_databases/
- **Purpose**: Historical database files
- **Files**:
  - `admin_panel.db`: Old admin database
  - `cms_core.db`: Old core database
  - `cms_database.db`: Old CMS database
- **Status**: Deprecated, kept for reference

### Documentation Directory (`docs/`)

#### docs/version_notes.txt
- **Purpose**: Version history notes
- **Contains**:
  - v1: Interface only
  - v2: Scrape function added

#### docs/installation_notes.txt
- **Purpose**: Installation instructions
- **Contains**:
  - Terminal shortcut (Ctrl + ~)
  - pip install commands
  - Playwright install
  - Environment path notes

## Design Decisions

### Why This Structure?

1. **Separation of Concerns**
   - Source code in `src/`
   - Data in `data/`
   - Archives in `archive/`
   - Docs in `docs/`

2. **Scalability**
   - Easy to add new scrapers
   - Database modules can be added
   - Clear versioning

3. **Maintainability**
   - Old versions preserved
   - Clear documentation
   - Logical organization

4. **Git-Friendly**
   - .gitignore properly configured
   - Large databases can be excluded
   - Clean repository

### Package Structure

- **src/**: Main package
  - **scrapers/**: Sub-package for scrapers
  - **database/**: Sub-package for DB operations
  - Each with `__init__.py` for proper imports

### Data Separation

- Active data (`data/`) separate from code
- Old data archived (`archive/old_databases/`)
- Makes backup and migration easier

## File Naming Conventions

- **Python files**: `lowercase_with_underscores.py`
- **Markdown files**: `UPPERCASE.md` (root) or descriptive names
- **Text files**: `lowercase_with_underscores.txt`
- **Databases**: `descriptive_name.db`

## Import Paths

From root directory:

```python
# Import main app
from src import app

# Import scraper
from src.scrapers import scrape_website

# Import from scrapers
from src.scrapers.playwright_scraper import scrape_website
```

## Running the Application

Always run from the root directory:

```bash
# Correct
streamlit run src/app.py

# Incorrect (will fail with import errors)
cd src && streamlit run app.py
```

## Future Structure Plans

### Potential Additions

```
src/
├── scrapers/
│   ├── requests_scraper.py    # Extract from app.py
│   └── selenium_scraper.py    # New scraper type
├── database/
│   ├── db_manager.py          # Database operations
│   └── models.py              # Data models
├── utils/
│   ├── url_utils.py           # URL handling
│   └── html_utils.py          # HTML processing
└── config/
    ├── settings.py            # Configuration
    └── constants.py           # Constants
```

### Testing Structure

```
tests/
├── __init__.py
├── test_scrapers.py
├── test_database.py
└── test_app.py
```

## Size Information

Current project size:
- Source code: ~20 KB
- Documentation: ~25 KB
- Dependencies: ~50 MB (when installed)
- Database: Variable (grows with usage)

## Maintenance

### Regular Tasks

1. **Update CHANGELOG.md** when adding features
2. **Keep README.md** synchronized with changes
3. **Archive old versions** before major updates
4. **Clean up databases** periodically
5. **Update requirements.txt** when adding dependencies

### Backup Strategy

- Git handles code versioning
- Archive old versions before updates
- Keep database backups in `archive/`
- Document all major changes

---

Last Updated: 2025
Version: 1.0.0
