import streamlit as st

def contact_page():
    # Push content down to clear the fixed navbar
    st.markdown('<div class="title-wrapper"></div>', unsafe_allow_html=True)
    
    # Page Header (Stays light to pop against the dark space background)
    st.markdown("""
        <div style="text-align: center;">
            <h3 style="color: #10b981; font-weight: 700; font-size: 1.1rem; margin-bottom: -10px; letter-spacing: 2px;">GET IN TOUCH</h3>
            <h1 class="main-title">
                <span style="color: #ffffff;">Contact </span><span style="color: #38bdf8;">Us</span>
            </h1>
            <p style="color: #cbd5e1; font-size: 1.15rem; max-width: 650px; margin: 0 auto 40px auto; line-height: 1.6;">
                Have questions about our climate data, want to collaborate on a publication, or need technical support? Drop us a message below!
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Custom CSS for the WHITE card and DARK headings
    st.markdown("""
        <style>
        /* 1. Ensure the form card is white */
        [data-testid="stForm"] {
            background-color: rgba(255, 255, 255, 0.95) !important;
            border: none !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
        }
        
        /* 2. CRITICAL FIX: Make the input headings (labels) deep blue so they are highly visible */
        [data-testid="stForm"] label p {
            color: #003366 !important; 
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            margin-bottom: 5px !important;
        }
        
        [data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input {
            background-color: #555 !important;
            color: #ffffff !important;
            border: 1px solid #cccccc !important;
            border-radius: 6px !important;
        }
        [data-testid="stTextArea"] textarea:focus, [data-testid="stTextInput"] input:focus {
            border-color: #0056b3 !important;
            background-color: #666 !important; /* Optional: turns white when they click to type */
            box-shadow: 0 0 5px rgba(0, 86, 179, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Center the form using a 3-column layout
    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        # The clear_on_submit=True empties the form after they click send
        with st.form(key="contact_form", clear_on_submit=True):
            # Changed heading to dark blue to contrast with the white card
            st.markdown("<h3 style='color: #003366; margin-top: 0; margin-bottom: 15px;'>Send a Message</h3>", unsafe_allow_html=True)
            
            name = st.text_input("Full Name", placeholder="Jane Doe")
            email = st.text_input("Email Address", placeholder="jane@institute.edu")
            subject = st.text_input("Subject", placeholder="Data Collaboration Inquiry")
            message = st.text_area("Message", placeholder="How can we help you?", height=150)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Full-width submit button
            submit_button = st.form_submit_button("Send Message", use_container_width=True)
            
            if submit_button:
                if name and email and message:
                    st.success("✅ Message sent successfully! Team Prometheus will get back to you soon.")
                else:
                    st.error("⚠️ Please fill out all required fields (Name, Email, and Message).")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
