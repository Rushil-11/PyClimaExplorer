import streamlit as st
import base64

def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

def render_navigation():
    img_base64 = get_image_base64("logo.png") 
    if img_base64:
        img_html = f'<img src="data:image/png;base64,{img_base64}" width="35" style="margin-right: 12px;">'
    else:
        img_html = '<span style="margin-right:10px;">🌍</span>'

    is_logged_in = st.session_state.get("logged_in", False)
    
    # Everything compressed into a single line to bypass Streamlit's Markdown parser
    if is_logged_in:
        nav_links = '<a href="?page=landing" target="_self">Home</a><a href="?page=dashboard" target="_self">Dashboard</a><a href="?page=about" target="_self">About</a><a href="?page=logout" class="reg-button" target="_self" style="background-color: #ef4444 !important; color: white !important;">Log Out</a>'
    else:
        nav_links = '<a href="?page=landing" target="_self">Home</a><a href="?page=about" target="_self">About</a><a href="?page=dashboard" target="_self">Dashboard</a><a href="?page=contact" target="_self">Contact Us</a><a href="?page=login" class="reg-button" target="_self">Login</a>'

    # The entire header compressed into a single line
    html_string = f'<div class="header-wrapper"><div style="display: flex; align-items: center; font-size: 24px; font-weight: 900;">{img_html}<span style="color: #38bdf8;">Py</span><span style="color: #10b981;">Clima</span><span style="color: #38bdf8;">Explorer</span></div><div class="nav-links">{nav_links}</div></div>'
    
    st.markdown(html_string, unsafe_allow_html=True)

def render_footer():
    # Footer compressed into a single line as well
    st.markdown('<div class="footer"><p style="margin: 0;">© 2026 PyClimaExplorer | Advanced Climate Modeling & Analysis</p></div>', unsafe_allow_html=True)