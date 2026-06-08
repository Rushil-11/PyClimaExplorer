import streamlit as st
from header import render_navigation, render_footer
from login import login_page
from landing import landing_page
from about import about_page
from contact import contact_page
from register import register_page
from database import create_tables
from dashboard import dashboard_page

st.set_page_config(page_title="PyClimaExplorer", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")
create_tables()

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_navigation()

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# --- 1. INITIALIZE SESSION STATES ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "guest_mode" not in st.session_state:
    st.session_state.guest_mode = False

# --- 2. GLOBAL POP-UP DIALOG ---
@st.dialog("👋 Welcome to PyClimaExplorer!")
def show_guest_popup():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <p style="color: #94a3b8; font-size: 1.05rem; line-height: 1.5;">
                Create a free account to save your workflows and access high-resolution NetCDF datasets, 
                or jump right in and explore the public data as a guest.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Free Account", type="primary", use_container_width=True):
            st.query_params["page"] = "login" 
            st.rerun()
    with col2:
        if st.button("Explore as Guest", use_container_width=True):
            st.session_state.guest_mode = True 
            st.query_params["page"] = "dashboard"
            st.rerun()

# --- THE ROUTER LOGIC ---
current_page = st.query_params.get("page", "landing")

if current_page == "logout":
    st.session_state.logged_in = False
    st.session_state.guest_mode = False 
    st.query_params.clear()
    st.rerun()

# --- 3. PUBLIC PAGES ---
if current_page == "landing":
    landing_page()
elif current_page == "about":
    about_page()
elif current_page == "contact":
    contact_page()
elif current_page == "register":
    register_page()

# --- 4. THE LOGIN GATE (The Interceptor) ---
elif not st.session_state.logged_in and not st.session_state.guest_mode:
    if current_page == "dashboard":
        # If they clicked Dashboard in the header (or anywhere else)
        # Render the landing page visually, then pop the dialog over it!
        landing_page() 
        show_guest_popup()
    else:
        # Default fallback for other protected pages
        login_page()

# --- 5. PROTECTED & GUEST PAGES ---
else:
    if current_page == "publications":
        if st.session_state.guest_mode:
            st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
            st.warning("⚠️ You must create a free account to view the Publications Database.")
            if st.button("Go to Login", type="primary"):
                st.query_params["page"] = "login"
                st.session_state.guest_mode = False
                st.rerun()
        else:
            st.markdown("<h2 style='color: #f8fafc; text-align: center; margin-top: 100px;'>Publications Database</h2>", unsafe_allow_html=True)
    else:
        dashboard_page()

st.markdown('</div>', unsafe_allow_html=True)
render_footer()