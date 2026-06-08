import streamlit as st
import time
from database import add_user

def register_page():
    # 3-column layout matching the Login page
    col1, spacer, col2 = st.columns([1.6, 0.1, 1])

    with col1:
        st.markdown('<div class="title-wrapper">', unsafe_allow_html=True)
        
        # Main Title
        st.markdown("""
            <h1 class="main-title">
                <span style="color: #ffffff;">Join </span><span style="color: #38bdf8;">Prometheus</span>
            </h1>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='color: #cbd5e1; font-size: 1.5rem; opacity: 0.9; line-height: 1.4;'>
                Create an account to unlock access to global <span style='color: #10b981; font-weight: bold;'>climate datasets</span>, 
                publish your interactive dashboards, and collaborate with researchers worldwide.
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Custom CSS to perfectly match the screenshot's styling
        st.markdown("""
            <style>
            /* 1. The White Card */
            [data-testid="stForm"] {
                background-color: #f8f9fa !important;
                border: none !important;
                box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
                border-radius: 12px !important;
            }
            
            /* 2. Dark Blue Heading */
            [data-testid="stForm"] h2 {
                color: #003366 !important;
            }
            
            /* 3. Faint Grey Labels (Email, Password, etc.) */
            [data-testid="stForm"] label p {
                color: #888888 !important; 
                font-size: 0.85rem !important;
                font-weight: 500 !important;
            }
            
            /* 4. Dark Grey Inputs with light text */
            [data-testid="stTextInput"] input {
                background-color: #262730 !important;
                color: #ffffff !important;
                border: 1px solid #333333 !important;
                border-radius: 6px !important;
            }
            [data-testid="stTextInput"] input:focus {
                border-color: #0068c9 !important;
                box-shadow: 0 0 0 1px #0068c9 !important;
            }
            
            /* 5. Bright Blue Submit Button */
            [data-testid="stFormSubmitButton"] button {
                background-color: #0068c9 !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 6px !important;
            }
            [data-testid="stFormSubmitButton"] button:hover {
                background-color: #0056b3 !important;
                color: #ffffff !important;
            }
            </style>
        """, unsafe_allow_html=True)

        with st.form(key="register_form", clear_on_submit=False):
            st.markdown("<h2 style='text-align: center; margin: 0 0 15px 0;'>Create Account</h2>", unsafe_allow_html=True)
        
            name = st.text_input("Full Name", placeholder="Jane Doe")
            email = st.text_input("Email", placeholder="researcher@example.com")
            institution = st.text_input("Institution / Affiliation", placeholder="University of ...")
            password = st.text_input("Password", type="password", placeholder="password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="password")
            
            # Full-width submit button
            submit_button = st.form_submit_button("Register", use_container_width=True)
            
            if submit_button:
                if not name or not email or not password or not confirm_password:
                    st.error("⚠️ Please fill out all required fields.")
                elif password != confirm_password:
                    st.error("⚠️ Passwords do not match.")
                else:
                    success = add_user(name, email, institution, password)
                    if success:
                        st.success("✅ Account created successfully! Redirecting to login...")
                        time.sleep(1.5) # Pause for 1.5 seconds so they can read the message
                        st.query_params["page"] = "home" # Update the URL to point to the login page
                        st.rerun() # Instantly reload the app!
                    else:
                        st.error("⚠️ That email is already registered.")

        # Sign-in link routed back to the login page
        st.markdown("""
            <div style='text-align: center; margin-top: 15px;'>
                <span style='color: #cbd5e1; font-size: 0.9rem;'>Already have an account?</span><br>
                <a href='?page=home' style='color: #38bdf8; font-weight: 700; text-decoration: none;'>Sign in here</a>
            </div>
        """, unsafe_allow_html=True)
