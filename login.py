import streamlit as st
from database import verify_user

def login_page():
    # 3-column layout
    col1, spacer, col2 = st.columns([1.6, 0.1, 1])

    with col1:
        # Wrapping the text in a div so we can push it down via CSS
        st.markdown('<div class="title-wrapper">', unsafe_allow_html=True)
        st.markdown('<h1 class="main-title">PyClimaExplorer</h1>', unsafe_allow_html=True)
        
        st.markdown("""
            <div style='color: white; font-size: 1.25rem; opacity: 0.9; line-height: 1.4;'>
                A collaborative platform for researchers to share, analyze, and 
                visualize <span style='color: #80d4ff; font-weight: bold;'>climate data</span> 
                across the globe.
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Using st.form guarantees a solid block we can style as a card
        with st.form(key="login_form", clear_on_submit=False):
            st.markdown("<h2 style='text-align: center; color: #003366; margin: 0 0 15px 0;'>Already a member?</h2>", unsafe_allow_html=True)
        
            email = st.text_input("Email", placeholder="researcher@example.com")
            password = st.text_input("Password", type="password", placeholder="password")
            
            c1, c2 = st.columns([1, 1])
            with c1:
                remember_me = st.checkbox("Remember me")
            with c2:
                st.markdown("<p style='text-align: right; margin-top: 5px;'><a href='#' style='color: #0056b3; font-weight: 600; font-size: 0.85rem;'>Forgot Password?</a></p>", unsafe_allow_html=True)

            submit_button = st.form_submit_button("Sign In", use_container_width=True)
            
            if submit_button:
                if verify_user(email, password):
                    st.session_state.logged_in = True
                    # --- CRITICAL ADDITION: Save the email for the Profile page ---
                    st.session_state.user_email = email 
                    st.rerun()
                else:
                    st.error("⚠️ Invalid email or password")
            
            st.markdown("""
                <div style='text-align: center; margin-top: 15px;'>
                    <span style='color: #666; font-size: 0.9rem;'>Don't have an account?</span><br>
                    <a href='?page=register' style='color: #0056B3; font-weight: 700;'>Register here</a>
                </div>
            """, unsafe_allow_html=True)