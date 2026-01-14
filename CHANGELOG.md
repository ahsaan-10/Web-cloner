# Changelog

All notable changes to the Web Cloner project are documented here.

## [1.0.0] - Current Version

### Added
- Full CMS functionality with admin panel
- Database integration using SQLite
- Two-panel editor with live preview
- Website management system (view, edit, delete)
- Save and retrieve cloned websites
- Real-time HTML editing
- Dual scraping methods (Requests + Playwright)

### Features
- BeautifulSoup + Requests scraper (default)
- Security cleanup (CSP removal, integrity checks)
- URL normalization (relative to absolute)
- Base tag injection for new tab links
- UTF-8 encoding enforcement
- User-Agent spoofing
- Session management
- Database persistence

### Project Structure
- Organized folder structure
- Separate directories for source, data, archive, docs
- Version history preservation
- Comprehensive documentation

## [0.3.0] - Version 3 (Archived)

### Added
- Download functionality for cloned HTML
- Dual scraping method selection
- Requests library as primary scraper
- Playwright as fallback option
- Better error handling
- Method selection UI

### Changed
- Switched from Playwright-first to Requests-first approach
- Improved UI with radio buttons for scraper selection
- Enhanced error messages

### Location
- `archive/versions/app_v3.txt`

## [0.2.0] - Version 2 (Archived)

### Added
- Playwright integration for web scraping
- Browser automation capabilities
- JavaScript rendering support
- Full HTML content extraction
- Better handling of dynamic websites

### Features
- Headless Chromium browser
- Network idle wait
- DOM content loaded detection
- Realistic viewport settings
- User agent spoofing

### Location
- `archive/versions/app_v2.txt`

## [0.1.0] - Version 1 (Archived)

### Added
- Initial UI design
- Streamlit framework setup
- Custom CSS styling
- Futuristic dark theme
- Orbitron and Inter fonts
- Gradient animations
- Input containers
- Button styling
- Preview placeholder

### Features
- Basic page layout
- URL input field
- Clone button (UI only)
- Preview section
- Responsive design
- Glassmorphism effects

### Location
- `archive/versions/app_v1.txt`

## Database Evolution

### Current Database
- `data/cloned_sites.db` - Active database with proper schema

### Archived Databases
- `archive/old_databases/admin_panel.db` - Old admin database
- `archive/old_databases/cms_core.db` - Old CMS core database
- `archive/old_databases/cms_database.db` - Old CMS database

## Documentation Updates

### Added
- README.md - Comprehensive project documentation
- QUICKSTART.md - Quick start guide
- CHANGELOG.md - This file
- requirements.txt - Python dependencies
- .gitignore - Git ignore rules

### Organized
- `docs/version_notes.txt` - Version history notes
- `docs/installation_notes.txt` - Installation instructions

## Project Organization

### Directory Structure Created
```
Web-cloner/
├── src/              # Source code
├── data/             # Active databases
├── archive/          # Old versions and databases
├── docs/             # Documentation
└── Root files        # Config and docs
```

### File Cleanup
- Removed empty `cms.py`
- Moved all version files to archive
- Organized database files
- Structured documentation

## Future Plans

### Planned Features
- [ ] User authentication system
- [ ] Multi-user support
- [ ] Export to PDF/DOCX
- [ ] Scheduled scraping
- [ ] Version diff viewer
- [ ] Proxy support
- [ ] Rate limiting
- [ ] REST API

### Improvements
- [ ] Better error handling
- [ ] Progress indicators
- [ ] Batch scraping
- [ ] Search functionality
- [ ] Tag system
- [ ] Categories

---

**Legend:**
- Added: New features
- Changed: Changes to existing functionality
- Deprecated: Features marked for removal
- Removed: Removed features
- Fixed: Bug fixes
- Security: Security improvements
