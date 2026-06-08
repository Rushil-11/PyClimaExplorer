import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import database as db

def generate_dummy_spatial_data(indicator, year):
    """Generates random global coordinate data to simulate NetCDF outputs."""
    np.random.seed(year)
    lats = np.random.uniform(-90, 90, 1000)
    lons = np.random.uniform(-180, 180, 1000)
    
    if indicator == "Temperature":
        # Hotter near equator, colder near poles
        values = 30 - np.abs(lats) * 0.7 + np.random.normal(0, 5, 1000)
        color_scale = "inferno"
    elif indicator == "Precipitation":
        values = np.random.exponential(50, 1000)
        color_scale = "Blues"
    else: # Wind Speed
        values = np.random.normal(15, 5, 1000)
        color_scale = "Viridis"
        
    return pd.DataFrame({"Latitude": lats, "Longitude": lons, "Value": values})

def generate_dummy_temporal_data(indicator):
    """Generates a 30-year time series trend."""
    years = np.arange(1990, 2026)
    if indicator == "Temperature":
        values = np.linspace(14.0, 15.5, len(years)) + np.random.normal(0, 0.2, len(years))
    elif indicator == "Precipitation":
        values = np.random.normal(1000, 50, len(years))
    else:
        values = np.random.normal(12, 1, len(years))
    return pd.DataFrame({"Year": years, "Value": values})

def dashboard_page():
    # --- DASHBOARD UI FIXES ---
    st.markdown("""
        <style>
        /* Change the background of the entire app ONLY when on the dashboard */
        [data-testid="stApp"] {
            background: linear-gradient(135deg, #020617 0%, #0f172a 100%) !important;
        }

        /* Force text inside the white forms and containers to be dark */
        [data-testid="stForm"] p, 
        [data-testid="stForm"] span, 
        [data-testid="stForm"] label p,
        [data-testid="stVerticalBlockBorderWrapper"] p {
            color: #1e293b !important; 
            font-weight: 600 !important;
        }
        
        /* Force headers inside containers to be dark */
        [data-testid="stForm"] h1, 
        [data-testid="stForm"] h2, 
        [data-testid="stForm"] h3,
        [data-testid="stVerticalBlockBorderWrapper"] h1,
        [data-testid="stVerticalBlockBorderWrapper"] h2,
        [data-testid="stVerticalBlockBorderWrapper"] h3 {
            color: #0f172a !important; 
        }

        /* Lighten the dark input boxes so they match the light card better */
        [data-testid="stForm"] [data-testid="stTextInput"] input {
            background-color: #f8fafc !important; 
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
            box-shadow: none !important;
        }
        
        /* Fix placeholder text color */
        [data-testid="stForm"] [data-testid="stTextInput"] input::placeholder {
            color: #94a3b8 !important;
        }
                
        /* --- SIDEBAR NAVIGATION PILLS --- */
        /* Hide the native radio button circles entirely */
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

        /* Style the labels as professional navigation pills */
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
            padding: 12px 16px !important;
            margin-bottom: 6px !important;
            border-radius: 6px !important;
            background-color: transparent !important;
            border: 1px solid transparent !important;
            transition: all 0.2s ease-in-out !important;
        }

        /* Hover state for the pills */
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
        }

        /* Text styling inside the pills */
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] p {
            font-weight: 600 !important;
            color: #475569 !important; 
            font-size: 0.95rem !important;
        }
        </style>
    """, unsafe_allow_html=True)
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        # Changed text to dark blue (#003366) to contrast with the new white background
        st.markdown("<h2 style='text-align: center; color: #003366; font-weight: 800;'>Control Panel</h2>", unsafe_allow_html=True)
        
        # Changed the horizontal line to a dark gray/black with low opacity
        st.markdown("<hr style='border-color: rgba(0,0,0,0.1); margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)
        
        # Native Streamlit radio buttons for clean, minimal navigation
        selected_tab = st.radio(
            "Navigation",
            ["Data Environment", "Analysis", "Compare", "Time Machine", "Profile"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.session_state.get("guest_mode", False):
            st.info("👀 Guest Mode Active. Some premium tools are disabled.")

    # --- 1. WELCOME SECTION ---
    if selected_tab == "Data Environment":
        st.markdown("<h1 style='color: #f8fafc;'>Welcome to the <span style='color: #10b981;'>Climate Analysis Dashboard</span></h1>", unsafe_allow_html=True)
        st.write("Configure your data environment before diving into the multidimensional analysis.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.subheader("📁 Choose Your Data Source")
            data_source = st.radio("Select input method:", ["🌐 Cloud NetCDF Data Cubes (Live)", "📂 Upload Your Own Files"], horizontal=True)
            
            if data_source == "📂 Upload Your Own Files":
                if st.session_state.get("guest_mode", False):
                    st.warning("Guests cannot upload custom NetCDF files. Please log in.")
                else:
                    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                    uploaded_file = st.file_uploader("Upload Climate Data", type=['nc', 'csv', 'hdf5'])
                    
                    if uploaded_file is not None:
                        # Log it to the database!
                        user_email = st.session_state.get("user_email")
                        if user_email:
                            file_ext = uploaded_file.name.split('.')[-1]
                            db.log_file_upload(user_email, uploaded_file.name, file_ext)
                            st.success(f"Successfully loaded `{uploaded_file.name}` into memory and saved to your profile!")
            else:
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                st.success("Connected to PyClimaExplorer Global NetCDF nodes. Data is ready to stream.")

    # --- 2. ANALYSIS SECTION ---
    elif selected_tab == "Analysis":
        st.title("Multidimensional Analysis")
        
        # Global Filters / Controls
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns(4)
            indicator = c1.selectbox("Climate Indicator", ["Temperature", "Precipitation", "Wind Speed"])
            time_slice = c2.slider("Time Slice (Year)", 1990, 2025, 2023)
            location = c3.selectbox("Location Focus", ["Global", "India", "Custom Coordinates"])
            
            # Show Lat/Lon only if Custom is selected
            if location == "Custom Coordinates":
                sub_c1, sub_c2 = c4.columns(2)
                lat = sub_c1.number_input("Lat", -90.0, 90.0, 0.0)
                lon = sub_c2.number_input("Lon", -180.0, 180.0, 0.0)
            else:
                c4.markdown("<div style='margin-top: 35px; color: #94a3b8; font-size: 0.9rem;'>Lat/Lon locked to preset</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabs for Spatial vs Temporal
        tab_spatial, tab_temporal = st.tabs(["🗺️ Spatial View (Maps)", "📈 Temporal View (Time Series)"])

        # --- SPATIAL VIEW ---
        with tab_spatial:
            df_spatial = generate_dummy_spatial_data(indicator, time_slice)
            
            # Setup map scope based on location filter
            map_scope = "world"
            if location == "India":
                map_scope = "asia" # Plotly doesn't have an India-only scope, so we zoom to Asia
                
            col_map1, col_map2 = st.columns(2)
            
            with col_map1:
                st.subheader("2D Projection")
                fig_2d = px.scatter_geo(
                    df_spatial, lat="Latitude", lon="Longitude", color="Value",
                    color_continuous_scale=px.colors.sequential.Plasma if indicator == "Temperature" else "Viridis",
                    projection="natural earth", scope=map_scope,
                    title=f"2D {indicator} Map ({time_slice})"
                )
                fig_2d.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)", geo=dict(bgcolor= 'rgba(0,0,0,0)'))
                st.plotly_chart(fig_2d, use_container_width=True)
                
            with col_map2:
                st.subheader("Curved Earth (3D)")
                fig_3d = px.scatter_geo(
                    df_spatial, lat="Latitude", lon="Longitude", color="Value",
                    color_continuous_scale=px.colors.sequential.Plasma if indicator == "Temperature" else "Viridis",
                    projection="orthographic", scope=map_scope,
                    title=f"3D {indicator} Globe ({time_slice})"
                )
                fig_3d.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor="rgba(0,0,0,0)", geo=dict(bgcolor= 'rgba(0,0,0,0)'))
                st.plotly_chart(fig_3d, use_container_width=True)

        # --- TEMPORAL VIEW ---
        with tab_temporal:
            df_temporal = generate_dummy_temporal_data(indicator)
            
            st.subheader(f"Historical Trend: {indicator} ({location})")
            
            # Interactive Line Chart
            fig_line = px.line(
                df_temporal, x="Year", y="Value", markers=True,
                title=f"{indicator} Changes from 1990 to 2025",
                template="plotly_dark"
            )
            # Make the line look sleek and match the theme
            fig_line.update_traces(line_color="#38bdf8", line_width=3, marker=dict(size=8, color="#10b981"))
            fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.2)")
            
            st.plotly_chart(fig_line, use_container_width=True)
            
            # Add a secondary chart for deeper "slice and dice" analytics
            st.subheader("Distribution Analysis")
            fig_box = px.box(
                df_spatial, y="Value", points="all", 
                title=f"Data Distribution for {time_slice}",
                template="plotly_dark"
            )
            fig_box.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.2)")
            st.plotly_chart(fig_box, use_container_width=True)

    # --- 3. PLACEHOLDER SECTIONS ---
    elif selected_tab == "Compare":
        st.title("Compare Datasets")
        st.info("Side-by-side anomaly comparison engine coming soon.")
        
    elif selected_tab == "Time Machine":
        st.title("Time Machine")
        st.info("Predictive modeling and past-climate reconstruction modules go here.")
        
    # --- 5. PROFILE SECTION ---
    elif selected_tab == "Profile":
        if st.session_state.get("guest_mode", False):
            st.warning("You are currently a Guest. Register an account to view your profile, save dashboard presets, and manage files.")
        else:
            user_email = st.session_state.get("user_email")
            user_details = db.get_user_details(user_email)

            if user_details:
                st.markdown(f"<h1 style='color: #f8fafc;'>Hello, <span style='color: #38bdf8;'>{user_details['name']}</span></h1>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                col1, col2 = st.columns([1, 1.5], gap="large")

                # Column 1: Account Details & Security
                with col1:
                    with st.container(border=True):
                        st.subheader("📋 Account Details")
                        st.markdown(f"**Name:** {user_details['name']}")
                        st.markdown(f"**Email:** {user_details['email']}")
                        st.markdown(f"**Institution:** {user_details['institution']}")

                    st.markdown("<br>", unsafe_allow_html=True)

                    with st.container(border=True):
                        st.subheader("🔒 Security")
                        with st.form("change_password_form", clear_on_submit=True):
                            st.write("Change your password")
                            current_pwd = st.text_input("Current Password", type="password")
                            new_pwd = st.text_input("New Password", type="password")
                            confirm_pwd = st.text_input("Confirm New Password", type="password")
                            
                            if st.form_submit_button("Update Password", type="primary", use_container_width=True):
                                if not db.verify_user(user_email, current_pwd):
                                    st.error("Current password is incorrect.")
                                elif new_pwd != confirm_pwd:
                                    st.error("New passwords do not match.")
                                elif len(new_pwd) < 6:
                                    st.error("New password must be at least 6 characters.")
                                else:
                                    db.change_password(user_email, new_pwd)
                                    st.success("Password updated successfully!")

                # Column 2: Upload History
                with col2:
                    with st.container(border=True):
                        st.subheader("📂 Upload History")
                        st.write("Files you have successfully parsed into PyClimaExplorer.")
                        
                        files = db.get_user_files(user_email)
                        if files:
                            # Convert DB results to a Pandas DataFrame for a beautiful table
                            df_files = pd.DataFrame(files, columns=["Filename", "Type", "Upload Date"])
                            st.dataframe(df_files, use_container_width=True, hide_index=True)
                        else:
                            st.info("You haven't uploaded any datasets yet. Head to the Welcome tab to get started.")
            else:
                st.error("Could not retrieve user details. Please try logging out and back in.")