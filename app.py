import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import sqlite3
import time
from datetime import datetime

# ============================================
# 1. DATABASE SETUP
# ============================================
def init_db():
    """Creates a local database file to store cloned websites."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            html_content TEXT,
            title TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_site_to_db(url, html, title=None):
    """Saves the cloned HTML to the database."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if title is None:
        title = urlparse(url).netloc or "Untitled Project"
    c.execute('INSERT INTO websites (url, html_content, title, created_at) VALUES (?, ?, ?, ?)',
              (url, html, title, timestamp))
    conn.commit()
    conn.close()

def get_all_sites():
    """Fetches list of all saved sites."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    c.execute('SELECT id, url, created_at, title FROM websites ORDER BY id DESC')
    data = c.fetchall()
    conn.close()
    return data

def get_html_by_id(site_id):
    """Gets HTML for a specific site."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    c.execute('SELECT html_content FROM websites WHERE id = ?', (site_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else ""

def get_site_by_id(site_id):
    """Gets full site data by ID."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    c.execute('SELECT id, url, html_content, title, created_at FROM websites WHERE id = ?', (site_id,))
    result = c.fetchone()
    conn.close()
    return result

def update_html_in_db(site_id, new_html):
    """Updates the HTML in the database."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    c.execute('UPDATE websites SET html_content = ? WHERE id = ?', (new_html, site_id))
    conn.commit()
    conn.close()

def delete_site_from_db(site_id):
    """Deletes a site from the database."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    c.execute('DELETE FROM websites WHERE id = ?', (site_id,))
    conn.commit()
    conn.close()

# Initialize DB
init_db()

# ============================================
# 2. SCRAPER FUNCTION
# ============================================
def scrape_website(url: str) -> tuple:
    """Scrapes website and returns (html_content, title, error)"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "identity",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=25, verify=True)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = soup.title.string if soup.title else urlparse(url).netloc

        # Cleanup Security
        for tag in soup.find_all('meta', attrs={'http-equiv': 'Content-Security-Policy'}):
            tag.decompose()
        for tag in soup.find_all(attrs={"integrity": True}):
            del tag['integrity']

        # Fix Links (Relative -> Absolute)
        for tag in soup.find_all(attrs={'href': True}):
            tag['href'] = urljoin(url, tag['href'])
        for tag in soup.find_all(attrs={'src': True}):
            tag['src'] = urljoin(url, tag['src'])

        # Base tag for new tabs
        if soup.head:
            base_tag = soup.new_tag("base", target="_blank")
            soup.head.insert(0, base_tag)

        return str(soup), title, None
    except Exception as e:
        return None, None, str(e)

# ============================================
# 3. PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="StreamClone - Web Clone Platform",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# 4. DESIGN SYSTEM (CSS INJECTION)
# ============================================
def inject_styles():
    """Inject the complete Clean SaaS design system."""
    st.markdown("""
    <style>
        /* ===== IMPORTS ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ===== ROOT VARIABLES ===== */
        :root {
            --bg-primary: #F8FAFC;
            --bg-secondary: #FFFFFF;
            --bg-tertiary: #F1F5F9;
            --text-primary: #0F172A;
            --text-secondary: #475569;
            --text-muted: #94A3B8;
            --accent-primary: #4F46E5;
            --accent-primary-hover: #4338CA;
            --accent-secondary: #7C3AED;
            --accent-gradient: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            --success: #10B981;
            --warning: #F59E0B;
            --error: #EF4444;
            --border-color: #E2E8F0;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --radius-full: 9999px;
        }

        /* ===== HIDE STREAMLIT DEFAULTS ===== */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}

        /* Remove default padding */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            max-width: 100% !important;
        }

        /* Main app background */
        .stApp {
            background-color: var(--bg-primary) !important;
        }

        /* ===== TYPOGRAPHY ===== */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif !important;
            color: var(--text-primary) !important;
            font-weight: 600 !important;
        }

        p, span, label, div {
            color: var(--text-secondary);
        }

        /* ===== CUSTOM HEADER ===== */
        .custom-header {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 16px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: sticky;
            top: 0;
            z-index: 1000;
            margin: -1rem -1rem 0 -1rem;
            width: calc(100% + 2rem);
        }

        .header-logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .header-logo-icon {
            width: 36px;
            height: 36px;
            background: var(--accent-gradient);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }

        .header-logo-text {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary) !important;
            letter-spacing: -0.5px;
        }

        .header-nav {
            display: flex;
            gap: 8px;
        }

        .nav-btn {
            padding: 8px 16px;
            border-radius: var(--radius-full);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            text-decoration: none;
        }

        .nav-btn:hover {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }

        .nav-btn.active {
            background: var(--accent-primary);
            color: white;
        }

        /* ===== HERO SECTION ===== */
        .hero-section {
            text-align: center;
            padding: 80px 20px 60px;
            max-width: 720px;
            margin: 0 auto;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            background: rgba(79, 70, 229, 0.1);
            border: 1px solid rgba(79, 70, 229, 0.2);
            border-radius: var(--radius-full);
            font-size: 13px;
            font-weight: 500;
            color: var(--accent-primary);
            margin-bottom: 24px;
        }

        .hero-title {
            font-size: 48px;
            font-weight: 700;
            line-height: 1.1;
            color: var(--text-primary) !important;
            margin-bottom: 16px;
            letter-spacing: -1.5px;
        }

        .hero-title-gradient {
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-subtitle {
            font-size: 18px;
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 40px;
        }

        /* ===== INPUT FIELD ===== */
        .url-input-container {
            background: var(--bg-secondary);
            border: 2px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: var(--shadow-lg);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
            max-width: 600px;
            margin: 0 auto 24px;
        }

        .url-input-container:focus-within {
            border-color: var(--accent-primary);
            box-shadow: var(--shadow-xl), 0 0 0 4px rgba(79, 70, 229, 0.1);
        }

        .stTextInput > div > div > input {
            background: transparent !important;
            border: none !important;
            padding: 12px 16px !important;
            font-size: 16px !important;
            color: var(--text-primary) !important;
            box-shadow: none !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: var(--text-muted) !important;
        }

        .stTextInput > label {
            display: none !important;
        }

        /* ===== BUTTONS ===== */
        .stButton > button {
            background: var(--accent-gradient) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-full) !important;
            padding: 12px 32px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.4) !important;
            letter-spacing: -0.2px !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.5) !important;
        }

        .stButton > button:active {
            transform: translateY(0) !important;
        }

        /* Secondary button style */
        .secondary-btn > button {
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
            box-shadow: var(--shadow-sm) !important;
        }

        .secondary-btn > button:hover {
            background: var(--bg-tertiary) !important;
            box-shadow: var(--shadow-md) !important;
        }

        /* Ghost button */
        .ghost-btn > button {
            background: transparent !important;
            color: var(--text-secondary) !important;
            box-shadow: none !important;
            padding: 8px 16px !important;
        }

        .ghost-btn > button:hover {
            background: var(--bg-tertiary) !important;
            color: var(--text-primary) !important;
            transform: none !important;
        }

        /* ===== PROJECT CARDS ===== */
        .project-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px;
            transition: all 0.2s ease;
            cursor: pointer;
            height: 100%;
        }

        .project-card:hover {
            border-color: var(--accent-primary);
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }

        .project-card-icon {
            width: 48px;
            height: 48px;
            background: var(--bg-tertiary);
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-bottom: 16px;
        }

        .project-card-title {
            font-size: 16px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .project-card-url {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 12px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .project-card-date {
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .project-card-actions {
            display: flex;
            gap: 8px;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid var(--border-color);
        }

        .action-btn {
            flex: 1;
            padding: 8px 12px;
            border-radius: var(--radius-sm);
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
            border: 1px solid var(--border-color);
            background: var(--bg-secondary);
            color: var(--text-secondary);
            text-align: center;
            text-decoration: none;
        }

        .action-btn:hover {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }

        .action-btn.primary {
            background: var(--accent-primary);
            border-color: var(--accent-primary);
            color: white;
        }

        .action-btn.primary:hover {
            background: var(--accent-primary-hover);
        }

        /* ===== EMPTY STATE ===== */
        .empty-state {
            text-align: center;
            padding: 80px 20px;
            background: var(--bg-secondary);
            border: 2px dashed var(--border-color);
            border-radius: var(--radius-lg);
            margin: 20px 0;
        }

        .empty-state-icon {
            font-size: 48px;
            margin-bottom: 16px;
            opacity: 0.5;
        }

        .empty-state-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 8px;
        }

        .empty-state-desc {
            font-size: 14px;
            color: var(--text-muted);
            margin-bottom: 24px;
        }

        /* ===== EDITOR WORKSPACE ===== */
        .editor-topbar {
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 0 -1rem;
            width: calc(100% + 2rem);
        }

        .breadcrumbs {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }

        .breadcrumb-item {
            color: var(--text-muted);
            text-decoration: none;
            cursor: pointer;
            transition: color 0.15s ease;
        }

        .breadcrumb-item:hover {
            color: var(--accent-primary);
        }

        .breadcrumb-separator {
            color: var(--text-muted);
        }

        .breadcrumb-current {
            color: var(--text-primary);
            font-weight: 500;
        }

        .editor-sidebar {
            background: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            padding: 20px;
            height: calc(100vh - 120px);
            overflow-y: auto;
        }

        .editor-canvas {
            background: var(--bg-tertiary);
            padding: 20px;
            height: calc(100vh - 120px);
            overflow: hidden;
        }

        .canvas-frame {
            background: var(--bg-secondary);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-xl);
            overflow: hidden;
            height: 100%;
        }

        /* ===== STATUS STEPS ===== */
        .status-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px;
            max-width: 480px;
            margin: 24px auto;
            box-shadow: var(--shadow-md);
        }

        .status-step {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 0;
            border-bottom: 1px solid var(--border-color);
        }

        .status-step:last-child {
            border-bottom: none;
        }

        .status-icon {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
        }

        .status-icon.pending {
            background: var(--bg-tertiary);
            color: var(--text-muted);
        }

        .status-icon.active {
            background: rgba(79, 70, 229, 0.1);
            color: var(--accent-primary);
            animation: pulse 1.5s infinite;
        }

        .status-icon.done {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .status-text {
            font-size: 14px;
            color: var(--text-secondary);
        }

        .status-text.active {
            color: var(--text-primary);
            font-weight: 500;
        }

        /* ===== SECTION HEADERS ===== */
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding: 0 4px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 600;
            color: var(--text-primary);
        }

        /* ===== EXPANDER STYLING ===== */
        .streamlit-expanderHeader {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            font-weight: 500 !important;
        }

        .streamlit-expanderContent {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border-color) !important;
            border-top: none !important;
            border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
        }

        /* ===== TEXT AREA ===== */
        .stTextArea > div > div > textarea {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
            font-size: 13px !important;
            color: var(--text-primary) !important;
        }

        .stTextArea > div > div > textarea:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        }

        /* ===== SELECTBOX ===== */
        .stSelectbox > div > div {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: var(--radius-md) !important;
        }

        /* ===== SUCCESS/ERROR MESSAGES ===== */
        .stSuccess {
            background: rgba(16, 185, 129, 0.1) !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important;
            border-radius: var(--radius-md) !important;
        }

        .stError {
            background: rgba(239, 68, 68, 0.1) !important;
            border: 1px solid rgba(239, 68, 68, 0.2) !important;
            border-radius: var(--radius-md) !important;
        }

        .stWarning {
            background: rgba(245, 158, 11, 0.1) !important;
            border: 1px solid rgba(245, 158, 11, 0.2) !important;
            border-radius: var(--radius-md) !important;
        }

        /* ===== SPINNER ===== */
        .stSpinner > div {
            border-color: var(--accent-primary) transparent transparent !important;
        }

        /* ===== COLUMNS GAP ===== */
        [data-testid="column"] {
            padding: 0 8px;
        }

        /* ===== TOOL PANEL ===== */
        .tool-panel {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 16px;
            margin-bottom: 12px;
        }

        .tool-panel-title {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            padding: 24px;
            color: var(--text-muted);
            font-size: 13px;
            border-top: 1px solid var(--border-color);
            margin-top: 40px;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 32px;
            }
            .hero-subtitle {
                font-size: 16px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================
# 5. MOCK DATA FOR DASHBOARD
# ============================================
def get_mock_projects():
    """Returns mock project data for UI demonstration."""
    return [
        {
            "id": 1,
            "title": "UITU Official Website",
            "url": "https://uitu.edu.pk",
            "created_at": "2025-01-15 14:30:00",
            "icon": "🎓"
        },
        {
            "id": 2,
            "title": "Stripe Landing Page",
            "url": "https://stripe.com",
            "created_at": "2025-01-14 10:15:00",
            "icon": "💳"
        },
        {
            "id": 3,
            "title": "Vercel Dashboard",
            "url": "https://vercel.com",
            "created_at": "2025-01-13 16:45:00",
            "icon": "▲"
        },
    ]

# ============================================
# 6. SESSION STATE INITIALIZATION
# ============================================
def init_session_state():
    """Initialize all session state variables."""
    if 'page' not in st.session_state:
        st.session_state.page = 'wizard'
    if 'scraped_html' not in st.session_state:
        st.session_state.scraped_html = None
    if 'scraped_url' not in st.session_state:
        st.session_state.scraped_url = None
    if 'scraped_title' not in st.session_state:
        st.session_state.scraped_title = None
    if 'editing_site_id' not in st.session_state:
        st.session_state.editing_site_id = None
    if 'clone_status' not in st.session_state:
        st.session_state.clone_status = None

init_session_state()

# ============================================
# 7. NAVIGATION HELPERS
# ============================================
def navigate_to(page, **kwargs):
    """Navigate to a different page with optional parameters."""
    st.session_state.page = page
    for key, value in kwargs.items():
        st.session_state[key] = value

# ============================================
# 8. RENDER FUNCTIONS
# ============================================
def render_header():
    """Render the custom header with navigation."""
    current_page = st.session_state.page

    st.markdown("""
    <div class="custom-header">
        <div class="header-logo">
            <div class="header-logo-icon">⚡</div>
            <span class="header-logo-text">StreamClone</span>
        </div>
        <div class="header-nav" id="header-nav">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation buttons using Streamlit
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 3])

    with col2:
        if st.button("Clone", key="nav_wizard", use_container_width=True,
                     type="primary" if current_page == 'wizard' else "secondary"):
            navigate_to('wizard')
            st.rerun()

    with col3:
        if st.button("Dashboard", key="nav_dashboard", use_container_width=True,
                     type="primary" if current_page == 'dashboard' else "secondary"):
            navigate_to('dashboard')
            st.rerun()

    with col4:
        if current_page == 'editor':
            st.markdown('<div class="ghost-btn">', unsafe_allow_html=True)
            if st.button("← Back", key="nav_back", use_container_width=True):
                navigate_to('dashboard')
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


def render_wizard():
    """Render the Clone Wizard / Landing Page."""

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">
            <span>✨</span>
            <span>Final Year Project 2025</span>
        </div>
        <h1 class="hero-title">
            Turn Any URL into a<br>
            <span class="hero-title-gradient">Live Replica</span>
        </h1>
        <p class="hero-subtitle">
            Clone any educational website into an editable CMS.
            Perfect for learning, prototyping, and building your portfolio.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # URL Input Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        url_input = st.text_input(
            "URL",
            placeholder="https://example.com",
            label_visibility="collapsed",
            key="url_input"
        )

        clone_clicked = st.button("⚡ Clone Website", use_container_width=True, key="clone_btn")

        if clone_clicked and url_input:
            # Add https if not present
            if not url_input.startswith(('http://', 'https://')):
                url_input = 'https://' + url_input

            # Show status container
            status_placeholder = st.empty()

            # Step 1: Fetching HTML
            status_placeholder.markdown("""
            <div class="status-container">
                <div class="status-step">
                    <div class="status-icon active">◉</div>
                    <span class="status-text active">Fetching HTML content...</span>
                </div>
                <div class="status-step">
                    <div class="status-icon pending">○</div>
                    <span class="status-text">Downloading CSS assets...</span>
                </div>
                <div class="status-step">
                    <div class="status-icon pending">○</div>
                    <span class="status-text">Hydrating DOM...</span>
                </div>
                <div class="status-step">
                    <div class="status-icon pending">○</div>
                    <span class="status-text">Finalizing clone...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.5)

            # Step 2: Downloading CSS
            status_placeholder.markdown("""
            <div class="status-container">
                <div class="status-step">
                    <div class="status-icon done">✓</div>
                    <span class="status-text">Fetching HTML content...</span>
                </div>
                <div class="status-step">
                    <div class="status-icon active">◉</div>
                    <span class="status-text active">Downloading CSS assets...</span>
                </div>
                <div class="status-step">
                    <div class="status-icon pending">○</div>
                    <span class="status-text">Hydrating DOM...</span>
                </div>
                <div class="status-step">
                    <div class="status-icon pending">○</div>
                    <span class="status-text">Finalizing clone...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Actually scrape
            html_content, title, error = scrape_website(url_input)

            if error:
                status_placeholder.empty()
                st.error(f"Failed to clone website: {error}")
            else:
                # Step 3: Hydrating
                status_placeholder.markdown("""
                <div class="status-container">
                    <div class="status-step">
                        <div class="status-icon done">✓</div>
                        <span class="status-text">Fetching HTML content...</span>
                    </div>
                    <div class="status-step">
                        <div class="status-icon done">✓</div>
                        <span class="status-text">Downloading CSS assets...</span>
                    </div>
                    <div class="status-step">
                        <div class="status-icon active">◉</div>
                        <span class="status-text active">Hydrating DOM...</span>
                    </div>
                    <div class="status-step">
                        <div class="status-icon pending">○</div>
                        <span class="status-text">Finalizing clone...</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.3)

                # Step 4: Done
                status_placeholder.markdown("""
                <div class="status-container">
                    <div class="status-step">
                        <div class="status-icon done">✓</div>
                        <span class="status-text">Fetching HTML content...</span>
                    </div>
                    <div class="status-step">
                        <div class="status-icon done">✓</div>
                        <span class="status-text">Downloading CSS assets...</span>
                    </div>
                    <div class="status-step">
                        <div class="status-icon done">✓</div>
                        <span class="status-text">Hydrating DOM...</span>
                    </div>
                    <div class="status-step">
                        <div class="status-icon done">✓</div>
                        <span class="status-text active">Clone complete!</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.3)

                # Store in session state
                st.session_state.scraped_html = html_content
                st.session_state.scraped_url = url_input
                st.session_state.scraped_title = title

                status_placeholder.empty()
                st.success(f"Successfully cloned **{title}** ({len(html_content):,} characters)")

    # Preview Section (if content available)
    if st.session_state.scraped_html:
        st.markdown("---")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="section-header">
                <span class="section-title">Preview</span>
            </div>
            """, unsafe_allow_html=True)

            # Action buttons
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                with st.expander("📄 View Source Code"):
                    st.code(st.session_state.scraped_html[:2000] + "...", language="html")

            with btn_col2:
                if st.button("💾 Save to Dashboard", use_container_width=True, key="save_btn"):
                    save_site_to_db(
                        st.session_state.scraped_url,
                        st.session_state.scraped_html,
                        st.session_state.scraped_title
                    )
                    st.success("Saved! View it in your Dashboard.")
                    st.balloons()

            with btn_col3:
                if st.button("✏️ Open in Editor", use_container_width=True, key="edit_btn"):
                    # Save first, then navigate
                    save_site_to_db(
                        st.session_state.scraped_url,
                        st.session_state.scraped_html,
                        st.session_state.scraped_title
                    )
                    sites = get_all_sites()
                    if sites:
                        navigate_to('editor', editing_site_id=sites[0][0])
                        st.rerun()

        # Preview frame
        col1, col2, col3 = st.columns([0.5, 3, 0.5])
        with col2:
            st.markdown('<div class="canvas-frame">', unsafe_allow_html=True)
            components.html(st.session_state.scraped_html, height=600, scrolling=True)
            st.markdown('</div>', unsafe_allow_html=True)


def render_dashboard():
    """Render the Project Dashboard with card grid."""

    st.markdown("""
    <div style="padding: 40px 20px;">
        <div class="section-header">
            <span class="section-title">Your Projects</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Get real sites from database
    saved_sites = get_all_sites()

    # If no real sites, show mock data option
    if not saved_sites:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📁</div>
            <div class="empty-state-title">No projects yet</div>
            <div class="empty-state-desc">Clone your first website to get started</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("⚡ Clone Your First Site", use_container_width=True, key="empty_clone"):
                navigate_to('wizard')
                st.rerun()

        # Show mock data toggle for demo
        st.markdown("---")
        if st.checkbox("Show demo projects (for presentation)", key="show_mock"):
            render_project_cards(get_mock_projects(), is_mock=True)
    else:
        # Convert DB results to card format
        projects = []
        icons = ["🌐", "🎓", "💼", "🛒", "📱", "💳", "▲", "🎨"]
        for i, site in enumerate(saved_sites):
            projects.append({
                "id": site[0],
                "title": site[3] if len(site) > 3 and site[3] else urlparse(site[1]).netloc,
                "url": site[1],
                "created_at": site[2],
                "icon": icons[i % len(icons)]
            })

        render_project_cards(projects, is_mock=False)


def render_project_cards(projects, is_mock=False):
    """Render project cards in a grid layout."""

    # Create rows of 3 cards
    for i in range(0, len(projects), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(projects):
                project = projects[i + j]
                with col:
                    st.markdown(f"""
                    <div class="project-card">
                        <div class="project-card-icon">{project['icon']}</div>
                        <div class="project-card-title">{project['title']}</div>
                        <div class="project-card-url">{project['url']}</div>
                        <div class="project-card-date">
                            <span>📅</span>
                            <span>{project['created_at']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Action buttons
                    if not is_mock:
                        btn_col1, btn_col2, btn_col3 = st.columns(3)
                        with btn_col1:
                            if st.button("👁️", key=f"preview_{project['id']}", help="Preview"):
                                st.session_state[f"show_preview_{project['id']}"] = True
                        with btn_col2:
                            if st.button("✏️", key=f"edit_{project['id']}", help="Edit"):
                                navigate_to('editor', editing_site_id=project['id'])
                                st.rerun()
                        with btn_col3:
                            if st.button("🗑️", key=f"delete_{project['id']}", help="Delete"):
                                delete_site_from_db(project['id'])
                                st.rerun()

                        # Show preview modal if triggered
                        if st.session_state.get(f"show_preview_{project['id']}", False):
                            with st.expander("Preview", expanded=True):
                                html_content = get_html_by_id(project['id'])
                                components.html(html_content, height=400, scrolling=True)
                                if st.button("Close Preview", key=f"close_preview_{project['id']}"):
                                    st.session_state[f"show_preview_{project['id']}"] = False
                                    st.rerun()


def render_editor():
    """Render the Visual Editor workspace."""

    site_id = st.session_state.editing_site_id

    if not site_id:
        st.warning("No project selected. Redirecting to dashboard...")
        navigate_to('dashboard')
        st.rerun()
        return

    site_data = get_site_by_id(site_id)
    if not site_data:
        st.error("Project not found.")
        navigate_to('dashboard')
        st.rerun()
        return

    site_id, url, html_content, title, created_at = site_data
    title = title or urlparse(url).netloc

    # Top Bar with Breadcrumbs
    st.markdown(f"""
    <div class="editor-topbar">
        <div class="breadcrumbs">
            <span class="breadcrumb-item" onclick="window.location.reload()">Dashboard</span>
            <span class="breadcrumb-separator">›</span>
            <span class="breadcrumb-current">{title}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Back button and Save button row
    top_col1, top_col2, top_col3 = st.columns([1, 4, 1])
    with top_col1:
        if st.button("← Back to Dashboard", key="back_to_dash"):
            navigate_to('dashboard')
            st.rerun()

    st.markdown("---")

    # Main Editor Layout (Holy Grail)
    editor_col, canvas_col = st.columns([1, 2])

    with editor_col:
        st.markdown("### 🛠️ Editor Tools")

        # Typography Tools
        with st.expander("📝 Typography", expanded=True):
            st.markdown('<div class="tool-panel">', unsafe_allow_html=True)
            font_family = st.selectbox(
                "Font Family",
                ["Inter", "Arial", "Georgia", "Times New Roman", "Courier New"],
                key="font_family"
            )
            font_size = st.slider("Base Font Size", 12, 24, 16, key="font_size")
            st.markdown('</div>', unsafe_allow_html=True)

        # Color Tools
        with st.expander("🎨 Colors", expanded=False):
            st.markdown('<div class="tool-panel">', unsafe_allow_html=True)
            primary_color = st.color_picker("Primary Color", "#4F46E5", key="primary_color")
            bg_color = st.color_picker("Background Color", "#FFFFFF", key="bg_color")
            text_color = st.color_picker("Text Color", "#0F172A", key="text_color")
            st.markdown('</div>', unsafe_allow_html=True)

        # Layout Tools
        with st.expander("📐 Layout", expanded=False):
            st.markdown('<div class="tool-panel">', unsafe_allow_html=True)
            max_width = st.slider("Max Width (px)", 800, 1400, 1200, key="max_width")
            padding = st.slider("Section Padding (px)", 0, 100, 40, key="padding")
            st.markdown('</div>', unsafe_allow_html=True)

        # Code Editor
        with st.expander("💻 Source Code", expanded=False):
            edited_html = st.text_area(
                "HTML Source",
                value=html_content,
                height=400,
                key="html_editor",
                label_visibility="collapsed"
            )

        # Save Button
        st.markdown("---")
        if st.button("💾 Save Changes", use_container_width=True, type="primary", key="save_changes"):
            # Get the edited HTML (either from text area or apply style changes)
            final_html = st.session_state.get("html_editor", html_content)

            # Apply style modifications
            soup = BeautifulSoup(final_html, 'html.parser')

            # Inject custom styles
            style_tag = soup.new_tag('style')
            style_tag.string = f"""
                body {{
                    font-family: '{font_family}', sans-serif !important;
                    font-size: {font_size}px !important;
                    background-color: {bg_color} !important;
                    color: {text_color} !important;
                }}
                a, .btn, button {{
                    color: {primary_color} !important;
                }}
                .container, main, article {{
                    max-width: {max_width}px !important;
                    padding: {padding}px !important;
                }}
            """
            if soup.head:
                soup.head.append(style_tag)

            final_html = str(soup)
            update_html_in_db(site_id, final_html)
            st.success("Changes saved successfully!")
            st.rerun()

    with canvas_col:
        st.markdown("### 👁️ Live Preview")

        # Apply live preview styles
        preview_html = html_content
        soup = BeautifulSoup(preview_html, 'html.parser')

        style_tag = soup.new_tag('style')
        style_tag.string = f"""
            body {{
                font-family: '{font_family}', sans-serif !important;
                font-size: {font_size}px !important;
                background-color: {bg_color} !important;
                color: {text_color} !important;
            }}
        """
        if soup.head:
            soup.head.append(style_tag)

        preview_html = str(soup)

        st.markdown('<div class="canvas-frame">', unsafe_allow_html=True)
        components.html(preview_html, height=700, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)


def render_footer():
    """Render the footer."""
    st.markdown("""
    <div class="footer">
        <p>StreamClone • Final Year Project 2025</p>
        <p>Built with Streamlit & Python</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# 9. MAIN APP
# ============================================
def main():
    """Main application entry point."""
    # Inject styles
    inject_styles()

    # Render header (navigation)
    render_header()

    # Route to appropriate page
    current_page = st.session_state.page

    if current_page == 'wizard':
        render_wizard()
    elif current_page == 'dashboard':
        render_dashboard()
    elif current_page == 'editor':
        render_editor()

    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
