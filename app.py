import streamlit as st
from header import render_navigation, render_footer
from landing import landing_page
from about import about_page
from dashboard import dashboard_page

st.set_page_config(page_title="PyClimaExplorer", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_navigation()

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# --- ROUTER LOGIC (No login/guest — direct access) ---
current_page = st.query_params.get("page", "landing")

if current_page == "landing":
    landing_page()
elif current_page == "about":
    about_page()
elif current_page == "dashboard":
    dashboard_page()
else:
    # Default fallback — show landing
    landing_page()

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
