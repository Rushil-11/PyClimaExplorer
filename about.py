import streamlit as st

def about_page():
    # --- EXTERNAL ASSETS & CSS ---
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        
        <style>
        h1, h2, h3, h4, p, span, div { font-family: 'Space Grotesk', sans-serif !important; }

        .gradient-text {
            background: linear-gradient(90deg, #ffffff 0%, #38bdf8 50%, #818cf8 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-size: 3.5rem; font-weight: 800; line-height: 1.2; margin-bottom: 10px;
        }

        @keyframes slideUpFade { 0% { opacity: 0; transform: translateY(30px); } 100% { opacity: 1; transform: translateY(0); } }
        .animate-slide-up { animation: slideUpFade 1s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        
        .glass-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(0, 20, 40, 0.2) 100%);
            backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.05); border-top: 1px solid rgba(255, 255, 255, 0.15); border-left: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px; padding: 35px; color: #f8fafc; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: transform 0.4s ease, box-shadow 0.4s ease; height: 100%;
        }
        .glass-card:hover { transform: translateY(-5px); border-top: 1px solid rgba(56, 189, 248, 0.5); box-shadow: 0 15px 35px rgba(0, 86, 179, 0.4); }

        .team-avatar {
            width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #0f172a, #1e293b);
            border: 2px solid #38bdf8; display: flex; align-items: center; justify-content: center;
            font-size: 2rem; color: #38bdf8; margin-bottom: 20px; transition: all 0.3s ease;
        }
        .glass-card:hover .team-avatar { transform: scale(1.1) rotate(5deg); box-shadow: 0 0 30px rgba(56, 189, 248, 0.6); }

        .role-tag {
            background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 12px; border-radius: 20px;
            font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
            display: inline-block; margin-bottom: 15px; border: 1px solid rgba(56, 189, 248, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    # --- HERO SECTION ---
    st.markdown("""
        <div class="animate-slide-up" style="text-align: center; padding-top: 60px; margin-bottom: 60px;">
            <div class="gradient-text">The Story of PyClimaExplorer</div>
            <p style="color: #94a3b8; font-size: 1.25rem; max-width: 800px; margin: 0 auto; line-height: 1.6;">
                Built in a single day. Driven by a crucial need for accessibility in global climate science.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- THE CHALLENGE SCOPE ---
    col_story1, col_story2 = st.columns(2, gap="large")
    
    with col_story1:
        st.markdown("""
            <div class="glass-card animate-slide-up" style="animation-delay: 0.1s;">
                <div style="font-size: 2.5rem; color: #38bdf8; margin-bottom: 20px;"><i class="fas fa-meteor"></i></div>
                <h2 style="font-size: 1.8rem; color: #f8fafc; margin-bottom: 15px;">The Challenge</h2>
                <p style="color: #94a3b8; font-size: 1.05rem; line-height: 1.7;">
                    Visualizing simulation output is crucial for both rigorous scientific understanding and vital public outreach. 
                    However, working with massive climate model data—such as NetCDF files from CESM or ERA5 reanalysis—often poses a massive technical barrier.
                    <br><br>
                    Our challenge was clear: <strong>Build a functional, rapid-prototype interactive visualizer.</strong> We needed a tool capable of loading heavy climate datasets and instantly producing multiple visualizations, from global heatmaps to temporal line plots.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    with col_story2:
        st.markdown("""
            <div class="glass-card animate-slide-up" style="animation-delay: 0.2s;">
                <div style="font-size: 2.5rem; color: #10b981; margin-bottom: 20px;"><i class="fas fa-bullseye"></i></div>
                <h2 style="font-size: 1.8rem; color: #f8fafc; margin-bottom: 15px;">The Mission</h2>
                <p style="color: #94a3b8; font-size: 1.05rem; line-height: 1.7;">
                    Leveraging the power of the Python data ecosystem, we built a web-based dashboard that bridges the gap between raw numbers and human understanding.
                    <br><br>
                    <strong>PyClimaExplorer</strong> serves two vital audiences: <strong>Researchers</strong> who need a fast, zero-friction environment for "quick looks" at multi-dimensional data, and the <strong>General Public</strong>, who need complex anomalies translated into a compelling, visual story about our changing planet.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 80px; margin-bottom: 40px; text-align: center;' class='animate-slide-up'><hr style='border-color: rgba(255,255,255,0.1); max-width: 600px; margin: 0 auto;'></div>", unsafe_allow_html=True)

    # --- TEAM PROMETHEUS SECTION ---
    st.markdown("""
        <div class="animate-slide-up" style="text-align: center; margin-bottom: 50px; animation-delay: 0.3s;">
            <h2 style="font-size: 3rem; color: #ffffff; margin-bottom: 10px; font-weight: 800;">Meet <span style="color: #38bdf8;">Team Prometheus</span></h2>
            <p style="color: #94a3b8; font-size: 1.15rem;">The engineers and designers who built PyClimaExplorer.</p>
        </div>
    """, unsafe_allow_html=True)

    team_cols = st.columns(4)

    with team_cols[0]:
        st.markdown("""
            <div class="glass-card animate-slide-up" style="animation-delay: 0.4s; text-align: center; padding: 30px 20px;">
                <div style="display: flex; justify-content: center;"><div class="team-avatar"><i class="fas fa-brain"></i></div></div>
                <h3 style="font-size: 1.4rem; color: #f8fafc; margin-bottom: 5px;">Rushil</h3>
                <div class="role-tag">The Brainstormer</div>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin: 0;">Drives the core strategy, identifying crucial climate data challenges and architecting the platform's vision.</p>
            </div>
        """, unsafe_allow_html=True)

    with team_cols[1]:
        st.markdown("""
            <div class="glass-card animate-slide-up" style="animation-delay: 0.5s; text-align: center; padding: 30px 20px;">
                <div style="display: flex; justify-content: center;"><div class="team-avatar"><i class="fas fa-bolt"></i></div></div>
                <h3 style="font-size: 1.4rem; color: #f8fafc; margin-bottom: 5px;">Ishit</h3>
                <div class="role-tag">The Idea Executer</div>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin: 0;">Bridges the gap between rapid-prototype concepts and actionable development roadmaps.</p>
            </div>
        """, unsafe_allow_html=True)

    with team_cols[2]:
        st.markdown("""
            <div class="glass-card animate-slide-up" style="animation-delay: 0.6s; text-align: center; padding: 30px 20px;">
                <div style="display: flex; justify-content: center;"><div class="team-avatar"><i class="fas fa-laptop-code"></i></div></div>
                <h3 style="font-size: 1.4rem; color: #f8fafc; margin-bottom: 5px;">Shubh</h3>
                <div class="role-tag">The Builder</div>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin: 0;">Engineers the backend Python data ecosystem, handling complex NetCDF processing and plotting mechanics.</p>
            </div>
        """, unsafe_allow_html=True)

    with team_cols[3]:
        st.markdown("""
            <div class="glass-card animate-slide-up" style="animation-delay: 0.7s; text-align: center; padding: 30px 20px;">
                <div style="display: flex; justify-content: center;"><div class="team-avatar"><i class="fas fa-pen-nib"></i></div></div>
                <h3 style="font-size: 1.4rem; color: #f8fafc; margin-bottom: 5px;">Vartika</h3>
                <div class="role-tag">The Designer</div>
                <p style="color: #94a3b8; font-size: 0.9rem; line-height: 1.5; margin: 0;">Designs intuitive, user-centric interfaces to ensure that complex climate datasets are accessible through a seamless digital experience</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)