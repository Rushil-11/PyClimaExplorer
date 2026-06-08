import streamlit as st
import streamlit.components.v1 as components

def landing_page():

    # --- EXTERNAL ASSETS & CSS ---
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        
        <style>
        /* Global Font Override */
        h1, h2, h3, p, span, div {
            font-family: 'Space Grotesk', sans-serif !important;
        }

        /* 1. Live Data Ticker (Seamless Loop Fix) */
        .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background-color: rgba(0, 15, 30, 0.6);
            backdrop-filter: blur(4px);
            border-bottom: 1px solid rgba(56, 189, 248, 0.2);
            padding: 8px 0;
            position: absolute;
            top: 0; left: 0; z-index: 50;
            display: flex; /* Flexbox helps keep items inline */
        }
        .ticker {
            display: flex;
            width: max-content;
            animation: ticker 40s linear infinite; /* Adjusted speed */
        }
        .ticker:hover {
            animation-play-state: paused; /* Pauses on hover so users can read it */
        }
        .ticker-item {
            display: inline-block;
            padding: 0 3rem;
            color: #38bdf8;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 1px;
            white-space: nowrap;
        }
        .ticker-item span { color: #f8fafc; margin-left: 5px; }
        .ticker-item .alert { color: #ef4444; }
        
        @keyframes ticker {
            0% { transform: translate3d(0, 0, 0); }
            /* Shift by exactly 50%. Since the content is doubled, 50% is the exact length of one set! */
            100% { transform: translate3d(-50%, 0, 0); } 
        }

        /* 2. Gradient Typography */
        .gradient-text {
            background: linear-gradient(90deg, #ffffff 0%, #38bdf8 50%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 4rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 15px;
            filter: drop-shadow(0px 4px 15px rgba(56, 189, 248, 0.2));
        }

        /* 3. Partner Logos / Social Proof */
        .partners-wrap {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            gap: 3rem;
            margin-top: 2.5rem;
            opacity: 0.6;
            transition: all 0.3s ease;
        }
        .partners-wrap:hover { opacity: 1; }
        .partner-logo {
            font-size: 1.1rem;
            font-weight: 700;
            color: #cbd5e1;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            letter-spacing: 1px;
        }

        /* 4. UPGRADED PREMIUM GLASSMORPHISM */
        @keyframes slideUpFade {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .animate-slide-up { animation: slideUpFade 1s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        
        .glass-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(0, 20, 40, 0.2) 100%);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            border-left: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 30px;
            color: #f8fafc;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease, border 0.4s ease;
            height: 100%;
        }
        .glass-card:hover {
            transform: translateY(-8px);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(0, 30, 60, 0.3) 100%);
            border-top: 1px solid rgba(56, 189, 248, 0.5);
            border-left: 1px solid rgba(56, 189, 248, 0.3);
            box-shadow: 0 15px 35px rgba(0, 86, 179, 0.4);
        }

        .icon-wrapper {
            font-size: 2.2rem;
            color: #38bdf8;
            margin-bottom: 18px;
            filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.4));
        }

        /* 5. Button Glow Micro-interaction */
        div[data-testid="column"]:nth-child(1) button {
            box-shadow: 0 0 15px rgba(0, 86, 179, 0.4);
            transition: all 0.3s ease !important;
        }
        div[data-testid="column"]:nth-child(1) button:hover {
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.6);
            transform: translateY(-2px);
        }
        
        /* Newsletter Form Styles */
        [data-testid="stForm"] [data-testid="stTextInput"] input {
            background-color: #334155 !important; 
            color: #ffffff !important;
            border: 1px solid #475569 !important;
            border-radius: 6px !important;
            padding: 10px !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
        }
        [data-testid="stForm"] [data-testid="stTextInput"] input::placeholder { color: #94a3b8 !important; }
        [data-testid="stForm"] label p { color: #003366 !important; font-weight: 700 !important; font-size: 0.95rem !important; }
        [data-testid="stForm"] { padding: 35px !important; border-radius: 16px !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- LIVE DATA TICKER ---
    # We save the items as a string, then duplicate it twice inside the HTML
    ticker_items = """
        <div class="ticker-item"><i class="fas fa-globe-americas"></i> Global Avg Temp: <span class="alert">+1.47°C</span></div>
        <div class="ticker-item"><i class="fas fa-smog"></i> Atmospheric CO2: <span>426.5 ppm</span></div>
        <div class="ticker-item"><i class="fas fa-water"></i> Sea Level Rise: <span class="alert">3.4 mm/yr</span></div>
        <div class="ticker-item"><i class="fas fa-icicles"></i> Arctic Ice Minimum: <span>4.23m sq km</span></div>
        <div class="ticker-item"><i class="fas fa-database"></i> NetCDF Nodes Active: <span>1,204</span></div>
    """

    st.markdown(f"""
        <div class="ticker-wrap">
            <div class="ticker">
                {ticker_items}
                {ticker_items} </div>
        </div>
        <div style='margin-top: 60px;'></div>
    """, unsafe_allow_html=True)

    # --- HERO SECTION ---
    st.markdown("""
        <div class="animate-slide-up" style="text-align: center; padding-top: 40px;">
            <div class="gradient-text">
                Understand Climate.<br>Explore Change.<br>Discover the Future.
            </div>
            <p style="color: #94a3b8; font-size: 1.2rem; max-width: 750px; margin: 0 auto 35px auto; line-height: 1.6;">
                Interactive climate analytics powered by Earth observation pipelines, NOAA matrices, 
                NetCDF data cubes, and real-time data science.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Buttons — direct to dashboard, no login popup
    _, col_btn1, col_btn2, _ = st.columns([2.5, 1.2, 1.2, 2.5])
    
    with col_btn1:
        if st.button("Explore Dashboard →", type="primary", use_container_width=True):
            st.query_params["page"] = "dashboard"
            st.rerun()
                
    with col_btn2:
        if st.button("Learn More", use_container_width=True):
            st.query_params["page"] = "about"
            st.rerun()

    # Citing NetCDF & Partners
    st.markdown("""
        <div class="partners-wrap animate-slide-up" style="animation-delay: 0.2s;">
            <div class="partner-logo"><i class="fas fa-satellite"></i> COPERNICUS</div>
            <div class="partner-logo"><i class="fas fa-rocket"></i> NASA</div>
            <div class="partner-logo"><i class="fas fa-water"></i> NOAA</div>
            <div class="partner-logo"><i class="fas fa-database"></i> NetCDF</div>
            <div class="partner-logo"><i class="fas fa-globe-europe"></i> ESA</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # --- THE 3D GLOBE ---
    globe_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style> 
            body { margin: 0; background-color: transparent; overflow: hidden; display: flex; justify-content: center; align-items: center; }
            #globeViz { width: 100%; height: 100%; cursor: grab; }
            #globeViz:active { cursor: grabbing; }
        </style>
        <script src="//unpkg.com/globe.gl"></script>
    </head>
    <body class="animate-fade-in">
        <div id="globeViz"></div>
        <script>
            const elem = document.getElementById('globeViz');
            const world = Globe()(elem)
                .globeImageUrl('//unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
                .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
                .showAtmosphere(true)
                .atmosphereColor('#38bdf8')
                .atmosphereAltitude(0.2)
                .backgroundColor('rgba(0,0,0,0)');

            world.controls().autoRotate = true;
            world.controls().autoRotateSpeed = 1.2;
            world.controls().minDistance = 200;
            world.controls().maxDistance = 400;
        </script>
    </body>
    </html>
    """
    # Restored to components.html so the JavaScript executes properly!
    components.html(globe_html, height=450)

    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

    # --- COPERNICUS STATS ---
    st.markdown("""
        <div class="glass-card animate-slide-up" style="text-align: center; margin-bottom: 2rem;">
            <h2 style="font-size: 2rem; margin-bottom: 10px;">2025 ranks as the <span style="color: #ef4444;">third warmest year</span> on record.</h2>
            <p style="color: #94a3b8; font-size: 1.1rem; margin: 0;">Following the unprecedented temperatures observed in 2023 and 2024.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="glass-card animate-slide-up" style="animation-delay: 0.2s; text-align: center;">
                <h1 style="font-size: 4rem; color: #f59e0b; margin: 0; line-height: 1; filter: drop-shadow(0 0 10px rgba(245, 158, 11, 0.3));">+1.47°C</h1>
                <h4 style="margin-top: 15px; color: #e2e8f0; font-weight: 600;">Above pre-industrial levels</h4>
                <hr style="border-color: rgba(255,255,255,0.08); margin: 20px 0;">
                <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">2025 was only marginally cooler than 2023, solidifying a clear, long-term warming trend.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="glass-card animate-slide-up" style="animation-delay: 0.3s; text-align: center;">
                <div style="font-size: 3rem; color: #ef4444; margin-bottom: 5px; filter: drop-shadow(0 0 10px rgba(239, 68, 68, 0.4));"><i class="fas fa-fire-flame-curved"></i></div>
                <h2 style="font-size: 1.8rem; color: #ef4444; margin: 0; line-height: 1;">Extreme Heat Stress</h2>
                <hr style="border-color: rgba(255,255,255,0.08); margin: 20px 0;">
                <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">Half of the globe experienced more days than average with at least strong heat stress in 2025.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)

    # --- PROBLEMS & ANOMALIES ---
    st.markdown("""
        <div style="text-align: center; margin-bottom: 40px;" class="animate-slide-up">
            <h2 style="font-size: 2.2rem; margin-bottom: 10px; color: white;">Climate Problems & Anomalies</h2>
            <p style="color: #94a3b8; font-size: 1.1rem;">Visualizing the real-world impacts of a rapidly shifting global baseline.</p>
        </div>
    """, unsafe_allow_html=True)

    problems = [
        ("fa-temperature-high", "Heatwaves", "Prolonged periods of excessively hot weather disrupting ecosystems."),
        ("fa-snowflake", "Cold Anomalies", "Sudden, extreme freezing events caused by destabilized polar vortexes."),
        ("fa-cloud-showers-water", "Rainfall Anomalies", "Severe droughts or unprecedented flooding due to shifted precipitation."),
        ("fa-water", "Ocean Warming", "Rising sea surface temperatures destroying coral reefs and marine life."),
        ("fa-fire", "Wildfires", "Increased frequency and intensity of forest fires across the globe."),
        ("fa-smog", "Air Pollution", "Trapped particulates and smog exacerbated by stagnant weather patterns.")
    ]

    p_cols1 = st.columns(3)
    for col, (icon, title, desc) in zip(p_cols1, problems[:3]):
        with col:
            st.markdown(f"""
                <div class="glass-card animate-slide-up">
                    <div class="icon-wrapper"><i class="fas {icon}"></i></div>
                    <h3 style="margin-bottom: 10px; font-size: 1.3rem; color: #f8fafc; font-weight: 700;">{title}</h3>
                    <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5; margin: 0;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    p_cols2 = st.columns(3)
    for col, (icon, title, desc) in zip(p_cols2, problems[3:]):
        with col:
            st.markdown(f"""
                <div class="glass-card animate-slide-up">
                    <div class="icon-wrapper"><i class="fas {icon}"></i></div>
                    <h3 style="margin-bottom: 10px; font-size: 1.3rem; color: #f8fafc; font-weight: 700;">{title}</h3>
                    <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.5; margin: 0;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)

    # --- NEWSLETTER SECTION ---
    st.markdown("<div style='margin-top: 80px;' class='animate-slide-up'></div>", unsafe_allow_html=True)

    with st.form(key="newsletter_form", clear_on_submit=True):
        st.markdown("<h2 style='color: #003366; font-size: 1.8rem; margin-bottom: 5px; margin-top: -10px;'><i class='fas fa-envelope-open-text'></i> Stay Updated</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #4b5563; font-size: 0.95rem; margin-bottom: 25px; line-height: 1.4;'>Get the latest planetary data and platform updates delivered directly to your inbox.</p>", unsafe_allow_html=True)
        
        email = st.text_input("Email Address", placeholder="jane@institute.edu", label_visibility="collapsed")
        
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        submit = st.form_submit_button("Subscribe", use_container_width=True)
        
        if submit:
            if email and "@" in email:
                st.success("Thanks for subscribing!")
            else:
                st.error("Please enter a valid email address.")

    st.markdown("<br><br><br>", unsafe_allow_html=True)
