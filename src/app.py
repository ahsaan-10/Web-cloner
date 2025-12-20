import streamlit as st
import streamlit.components.v1
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import sqlite3
import sys
import asyncio
from datetime import datetime

# ============================================
# 1. DATABASE SETUP (The Memory)
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
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_site_to_db(url, html):
    """Saves the cloned HTML to the database."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO websites (url, html_content, created_at) VALUES (?, ?, ?)', 
              (url, html, timestamp))
    conn.commit()
    conn.close()

def get_all_sites():
    """Fetches list of all saved sites."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    c.execute('SELECT id, url, created_at FROM websites ORDER BY id DESC')
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

def update_html_in_db(site_id, new_html):
    """Updates the HTML in the database."""
    conn = sqlite3.connect('cloned_sites.db')
    c = conn.cursor()
    c.execute('UPDATE websites SET html_content = ? WHERE id = ?', (new_html, site_id))
    conn.commit()
    conn.close()

# Initialize DB immediately
init_db()

# ============================================
# 2. SCRAPER FUNCTION (Identity Fix Included)
# ============================================
def scrape_website(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "identity", # Force plain text (No gibberish)
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=25, verify=True)
        response.raise_for_status()
        response.encoding = 'utf-8' # Force UTF-8
            
        soup = BeautifulSoup(response.text, "html.parser")

        # Cleanup Security
        for tag in soup.find_all('meta', attrs={'http-equiv': 'Content-Security-Policy'}): tag.decompose()
        for tag in soup.find_all(attrs={"integrity": True}): del tag['integrity']

        # Fix Links (Relative -> Absolute)
        for tag in soup.find_all(attrs={'href': True}): tag['href'] = urljoin(url, tag['href'])
        for tag in soup.find_all(attrs={'src': True}): tag['src'] = urljoin(url, tag['src'])
        
        # Base tag for new tabs
        if soup.head:
            base_tag = soup.new_tag("base", target="_blank")
            soup.head.insert(0, base_tag)

        return str(soup)
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================
# 3. PAGE CONFIG & STYLING
# ============================================
st.set_page_config(
    page_title="AI Website Cloner & Admin Panel",
    page_icon="🛠️",
    layout="wide", # Wide layout for better editing
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Inter:wght@300;400;500;600&display=swap');
    
    .stApp { background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%); }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #7b2cbf, #00d4ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 3s ease infinite;
    }
    
    @keyframes gradient-shift { 0% { background-position: 0% center; } 100% { background-position: 0% center; } }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #a0a0b0;
        margin-bottom: 2rem;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: rgba(10, 10, 20, 0.8) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        color: white !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%) !important;
        color: white !important;
        border: none !important;
        font-family: 'Orbitron', monospace !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 4. ADMIN PANEL (DIRECT ACCESS)
# ============================================

# Sidebar Navigation
with st.sidebar:
    st.title("🛠️ Admin Panel")
    st.info("Direct Access Mode (No Login)")
    menu = st.radio("Navigation Menu", ["Clone New Site", "Manage Saved Sites"])
    st.divider()
    st.caption("Final Year Project • 2025")

# --- TAB A: CLONE NEW SITE (Your Original Tool) ---
if menu == "Clone New Site":
    st.markdown('<h1 class="main-title">AI Website Cloner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Clone any educational website into an editable CMS</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        url_input = st.text_input("Enter Website URL", placeholder="https://uitu.edu.pk")
        clone_button = st.button("⚡ CLONE WEBSITE", use_container_width=True)

    if clone_button and url_input:
        with st.spinner("🔄 Cloning website..."):
            html_content = scrape_website(url_input)
            
            if html_content.startswith("Error"):
                st.error(html_content)
            else:
                st.session_state["scraped_html"] = html_content
                st.session_state["scraped_url"] = url_input
                st.success(f"✅ Successfully cloned! {len(html_content):,} chars.")

    # Preview & Save Section
    if "scraped_html" in st.session_state:
        st.subheader("Preview")
        with st.expander("Show Source Code", expanded=False):
            st.code(st.session_state["scraped_html"][:1000] + "...", language="html")
        
        # --- SAVE BUTTON ---
        if st.button("💾 SAVE TO CMS DATABASE", type="primary"):
            save_site_to_db(st.session_state["scraped_url"], st.session_state["scraped_html"])
            st.balloons()
            st.success("Website Saved! Go to 'Manage Saved Sites' to edit it.")

        # Live Preview
        st.components.v1.html(st.session_state["scraped_html"], height=600, scrolling=True)

# --- TAB B: MANAGE SAVED SITES (The CMS Editor) ---
elif menu == "Manage Saved Sites":
    st.title("📝 Content Management System")
    st.markdown("Select a cloned website from the database to edit its content.")
    
    saved_sites = get_all_sites()
    
    if not saved_sites:
        st.warning("No saved websites found. Go to 'Clone New Site' to add one first.")
    else:
        # 1. Select Site Dropdown
        options = {f"{site[1]} (ID: {site[0]}) - {site[2]}": site[0] for site in saved_sites}
        selected_label = st.selectbox("Select Website to Edit", list(options.keys()))
        site_id = options[selected_label]
        
        # 2. Get HTML Content from DB
        current_html = get_html_by_id(site_id)
        
        # 3. Editor Interface
        col_edit, col_view = st.columns([1, 1])
        
        with col_edit:
            st.subheader("✏️ Code Editor")
            # Text Area for Editing
            new_html = st.text_area("Edit Source Code", value=current_html, height=800)
            
            # Update Button
            if st.button("💾 Update Website Changes", type="primary", use_container_width=True):
                update_html_in_db(site_id, new_html)
                st.toast("Changes Saved Successfully!", icon="✅")
                # We do not rerun immediately to avoid losing scroll position, 
                # but the preview will update on next interaction.
                st.success("Website Updated!")
        
        with col_view:
            st.subheader("👁️ Live Result")
            # Live Preview of the Edited Code
            st.components.v1.html(new_html, height=800, scrolling=True)