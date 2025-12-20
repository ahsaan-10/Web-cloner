import streamlit as st
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import time

# ============================================
# 1. PAGE CONFIGURATION
# (Must be the very first Streamlit command)
# ============================================
st.set_page_config(
    page_title="AI Website Cloner",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# 2. ROBUST SCRAPER FUNCTION
# ============================================
def scrape_website(url: str) -> str:
    """
    Scrapes a website using Playwright with robust error handling.
    Fixed: SSL errors, Timeout errors, and Detection evasion.
    """
    with sync_playwright() as p:
        # Launch headless browser
        browser = p.chromium.launch(headless=True)
        
        # Create context with anti-detection settings
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            ignore_https_errors=True,  # Fix for SSL/Certificate errors
            bypass_csp=True            # Bypass Content Security Policy
        )
        
        page = context.new_page()
        
        try:
            # Navigate to URL
            # Changed 'networkidle' to 'domcontentloaded' to prevent infinite hanging
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait a few seconds for JavaScript to render content
            time.sleep(3) 
            
            # Extract HTML
            html_content = page.content()
            
        except PlaywrightTimeout:
            # If it times out, grab whatever loaded so far instead of crashing
            st.warning("⚠️ The page took too long to load fully, but we captured what was available.")
            html_content = page.content()
            
        finally:
            # Always close browser resources
            context.close()
            browser.close()
        
        return html_content

# ============================================
# 3. CUSTOM CSS STYLING
# ============================================
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0f0f1a 100%);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Title styling */
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00d4ff, #7b2cbf, #00d4ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient-shift 3s ease infinite;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }
    
    /* Subtitle styling */
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        text-align: center;
        color: #a0a0b0;
        margin-bottom: 3rem;
        letter-spacing: 0.5px;
    }
    
    /* Input container */
    .input-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background: rgba(10, 10, 20, 0.8) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.8rem 1.2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #606080 !important;
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Orbitron', monospace !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 2.5rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 212, 255, 0.4) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Preview card styling */
    .preview-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px dashed rgba(0, 212, 255, 0.3);
        border-radius: 16px;
        padding: 4rem 2rem;
        margin-top: 2rem;
        text-align: center;
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }
    
    .preview-card:hover {
        border-color: rgba(0, 212, 255, 0.5);
        background: rgba(255, 255, 255, 0.03);
    }
    
    .preview-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .preview-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #606080;
        font-weight: 400;
    }
    
    /* Decorative elements */
    .glow-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, #7b2cbf, transparent);
        margin: 2rem auto;
        width: 60%;
        border-radius: 2px;
    }
    
    /* Label styling */
    .stTextInput > label {
        font-family: 'Inter', sans-serif !important;
        color: #a0a0b0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    
    /* Footer styling */
    .footer-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #404050;
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 4. UI LAYOUT
# ============================================

st.markdown('<h1 class="main-title">AI Website Cloner</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Clone any educational website into an editable CMS</p>', unsafe_allow_html=True)
st.markdown('<div class="glow-line"></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input Container
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        url_input = st.text_input(
            "Enter Website URL",
            placeholder="https://example.com",
            label_visibility="visible"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        clone_button = st.button("⚡ CLONE WEBSITE", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# 5. EXECUTION LOGIC
# ============================================
if clone_button:
    if url_input:
        if not url_input.startswith(("http://", "https://")):
            st.error("⚠️ Please enter a valid URL starting with http:// or https://")
        else:
            with st.spinner("🔄 Cloning website... Please wait..."):
                try:
                    # Reset previous data
                    if "scraped_html" in st.session_state:
                        del st.session_state["scraped_html"]

                    # Scrape
                    html_content = scrape_website(url_input)
                    
                    if not html_content or len(html_content) < 100:
                        st.error("❌ Failed to retrieve content. The website might be blocking access.")
                    else:
                        st.session_state["scraped_html"] = html_content
                        st.session_state["scraped_url"] = url_input
                        st.success(f"✅ Successfully cloned! Retrieved {len(html_content):,} characters of HTML.")
                        
                except Exception as e:
                    st.error(f"❌ Critical Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a URL first.")

# ============================================
# 6. PREVIEW SECTION
# ============================================
st.markdown("<br>", unsafe_allow_html=True)

if "scraped_html" in st.session_state and st.session_state["scraped_html"]:
    st.markdown("""
    <div class="preview-card" style="padding: 1.5rem; text-align: left;">
        <p style="color: #00d4ff; font-family: 'Orbitron', monospace; margin-bottom: 1rem;">
            📄 HTML PREVIEW
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display HTML in an expandable code block
    with st.expander(f"🌐 Source from: {st.session_state.get('scraped_url', 'Unknown')}", expanded=True):
        st.code(st.session_state["scraped_html"][:5000] + "...", language="html")
    
    # Show stats
    st.info(f"📊 Total HTML length: {len(st.session_state['scraped_html']):,} characters")
else:
    # Placeholder when empty
    st.markdown("""
    <div class="preview-card">
        <div class="preview-icon">🌐</div>
        <p class="preview-text">Preview will appear here</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-text">
    Final Year Project • AI Website Cloner • 2025
</div>
""", unsafe_allow_html=True)