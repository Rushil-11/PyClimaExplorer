import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import xarray as xr
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import base64

# --- Repo_1 imports for 3D Globe & Graphs ---
from modules.data_loader import load_temperature, load_precipitation, load_pressure
from modules.visualization import create_globe, create_timeseries

# ── Dataset Registry (from Repo_2 — for 2D Heatmap & Comparison) ─────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

DATASETS = {
    "Air Temperature (NCEP)":   {"file": "air.mon.mean.nc",   "var": "air",   "unit": "C",       "label": "Temperature (C)",   "scale": 1.0},
    "Wind Speed U-component":   {"file": "uwnd.mon.mean.nc",  "var": "uwnd",  "unit": "m/s",     "label": "U-Wind (m/s)",       "scale": 1.0},
    "Precipitation Rate":       {"file": "sample_data.nc",    "var": "prate", "unit": "mm/day",  "label": "Precip (mm/day)",    "scale": 86400.0},
}

@st.cache_data
def load_nc(filename, scale=1.0):
    path = os.path.join(DATA_DIR, filename)
    ds = xr.open_dataset(path)
    return ds, scale

# Pre-load all datasets at startup (uses cache after first load)
all_ds = {name: load_nc(info["file"], info["scale"]) for name, info in DATASETS.items()}


# ── Repo_2 Helper functions ──────────────────────────────────────────────────
def get_slice(dataset, variable, year, month, scale=1.0):
    """Get a single month's lat/lon slice, applying unit scale."""
    t  = dataset.sel(time=f"{year}-{month:02d}", method="nearest")
    da = t[variable] * scale
    return da

def slice_to_df(data_array, var_name):
    """Convert 2D DataArray to a DataFrame for plotting."""
    df = data_array.to_dataframe().reset_index().dropna(subset=[var_name])
    return df

def global_mean_timeseries(dataset, variable):
    """Return a DataFrame with monthly global mean over time."""
    gmean = dataset[variable].mean(dim=['lat', 'lon'])
    df = gmean.to_dataframe().reset_index()
    df['time'] = pd.to_datetime(df['time'])
    return df

def annual_mean_timeseries(dataset, variable):
    """Return annual mean time series."""
    df = global_mean_timeseries(dataset, variable)
    df['year'] = df['time'].dt.year
    return df.groupby('year')[variable].mean().reset_index()

def get_color_config(var_name, df, col):
    """Return (colorscale, vmin, vmax) appropriate for the variable type."""
    q02 = float(df[col].quantile(0.02))
    q98 = float(df[col].quantile(0.98))
    if var_name == 'uwnd':
        bound = max(abs(q02), abs(q98))
        return 'RdBu_r', -bound, bound
    elif var_name == 'prate':
        return 'Blues', 0.0, max(q98, 1.0)
    else:
        return 'RdBu_r', q02, q98


def dashboard_page():
    # --- DASHBOARD UI STYLES ---
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
        st.markdown("<h2 style='text-align: center; color: #003366; font-weight: 800;'>Control Panel</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(0,0,0,0.1); margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)
        
        # Only 3 options: Analysis, Comparison, Time Story
        selected_tab = st.radio(
            "Navigation",
            ["🔬 Analysis", "📊 Comparison", "🎬 Time Story"],
            label_visibility="collapsed"
        )
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════
    # TAB 1 — ANALYSIS (2D from Repo_2, 3D from Repo_1, Graphs from Repo_1)
    # ═══════════════════════════════════════════════════════════════════
    if selected_tab == "🔬 Analysis":
        st.markdown("<h1 style='color: #f8fafc;'>Multidimensional <span style='color: #10b981;'>Analysis</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Explore climate data through 2D heatmaps and 3D globe visualizations side by side.</p>", unsafe_allow_html=True)
        
        # --- Controls ---
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            
            # Dataset selector for 2D (Repo_2 style)
            dataset_name = c1.selectbox("Dataset", list(DATASETS.keys()))
            info = DATASETS[dataset_name]
            ds_2d, _scale = all_ds[dataset_name]
            var = info["var"]
            unit = info["unit"]
            
            # Time selection
            times = pd.DatetimeIndex(ds_2d['time'].values)
            years = sorted(times.year.unique())
            sel_year = c2.slider("Year", int(years[0]), int(years[-1]), int(years[-1]))
            sel_month = c3.select_slider("Month", list(range(1, 13)),
                                          format_func=lambda m: ["Jan","Feb","Mar","Apr","May","Jun",
                                                                   "Jul","Aug","Sep","Oct","Nov","Dec"][m-1])
        
        st.markdown("<br>", unsafe_allow_html=True)

        # --- Variable mapping for Repo_1 3D Globe ---
        variable_map = {
            "Air Temperature (NCEP)": ("Temperature", "temperature", load_temperature),
            "Wind Speed U-component": ("Pressure", "pressure", load_pressure),
            "Precipitation Rate": ("Precipitation", "precipitation", load_precipitation),
        }
        repo1_label, repo1_var, repo1_loader = variable_map[dataset_name]

        # ── 2D + 3D Side by Side ──
        col_2d, col_3d = st.columns(2)

        # --- LEFT: 2D Heatmap from Repo_2 ---
        with col_2d:
            st.subheader("🗺️ 2D Global Heatmap")
            try:
                scale = info["scale"]
                sliced = get_slice(ds_2d, var, sel_year, sel_month, scale)
                df_map = slice_to_df(sliced, var)

                cscale, vmin, vmax = get_color_config(var, df_map, var)

                fig_2d = px.scatter_geo(
                    df_map, lat='lat', lon='lon', color=var,
                    color_continuous_scale=cscale,
                    range_color=[vmin, vmax],
                    projection='natural earth',
                    labels={var: unit},
                    title=f"{dataset_name} — {sel_year}/{sel_month:02d}",
                    hover_data={'lat': ':.1f', 'lon': ':.1f', var: ':.2f'}
                )
                fig_2d.update_traces(marker=dict(size=3, opacity=0.7))
                fig_2d.update_layout(
                    height=520, 
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Space Grotesk', color='#e2e8f0'),
                    coloraxis_colorbar=dict(
                        title=dict(text=unit, font=dict(color='#e2e8f0', size=12)),
                        tickfont=dict(color='#e2e8f0', size=11),
                        outlinewidth=1, outlinecolor='#334155'
                    ),
                    geo=dict(
                        bgcolor='rgba(0,0,0,0)', showocean=True, oceancolor='#0c4a6e',
                        showland=True, landcolor='#1e3a5f',
                        showcoastlines=True, coastlinecolor='#38bdf8', showframe=False,
                    )
                )
                st.plotly_chart(fig_2d, use_container_width=True, theme=None)
            except Exception as e:
                st.error(f"Could not render 2D map: {e}")

        # --- RIGHT: 3D Globe from Repo_1 ---
        with col_3d:
            st.subheader("🌍 3D Globe View")
            try:
                # Find matching time index for 3D Globe based on selected year and month
                times_3d = pd.DatetimeIndex(ds_2d['time'].values)
                matching_indices = np.where((times_3d.year == sel_year) & (times_3d.month == sel_month))[0]
                time_index = int(matching_indices[0]) if len(matching_indices) > 0 else 0

                # Load from Repo_1 data_loader using calculated time_index
                ds_3d, df_3d = repo1_loader(time_index)
                fig_3d = create_globe(df_3d, repo1_var)
                
                # Restyle to match the dark theme
                fig_3d.update_layout(
                    height=520,
                    paper_bgcolor='rgba(0,0,0,0)',
                    geo=dict(
                        projection_type="orthographic",
                        showland=True,
                        landcolor="rgb(30,58,95)",
                        showocean=True,
                        oceancolor="rgb(12,74,110)",
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                st.plotly_chart(fig_3d, use_container_width=True, theme=None)
            except Exception as e:
                st.error(f"Could not render 3D globe: {e}")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")

        # ── Graphs from Repo_1 (below the 2D/3D views) ──
        st.markdown("<h2 style='color: #f8fafc;'>📈 Trend Analysis & <span style='color: #38bdf8;'>Context</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Global trends and seasonal patterns from the full dataset timeline.</p>", unsafe_allow_html=True)

        # --- Annual Trend (from Repo_2's Global Context section) ---
        col_t1, col_t2 = st.columns([2, 1])

        with col_t1:
            try:
                ann_df = annual_mean_timeseries(ds_2d, var)
                ann_df[var] *= info["scale"]
                
                fig_annual = px.line(ann_df, x='year', y=var,
                                 labels={'year': 'Year', var: unit},
                                 title=f"Annual Global Mean (1948–2026)")
                trend = np.poly1d(np.polyfit(ann_df['year'], ann_df[var], 1))(ann_df['year'])
                fig_annual.add_trace(go.Scatter(x=ann_df['year'], y=trend, mode='lines',
                                          name='Long-term Trend', line=dict(color='#ef4444', dash='dash', width=2)))
                fig_annual.add_vline(x=sel_year, line_width=2, line_dash="dash", line_color="#10b981")
                fig_annual.update_layout(
                    height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.2)',
                    font=dict(family='Space Grotesk', color='#e2e8f0'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.05)'), 
                    yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                    margin=dict(l=0, r=0, t=40, b=0),
                    legend=dict(font=dict(color='#e2e8f0'))
                )
                st.plotly_chart(fig_annual, use_container_width=True, theme=None)
            except Exception as e:
                st.error(f"Could not render annual trend: {e}")

        with col_t2:
            try:
                this_year_ds = ds_2d[var].sel(time=slice(f"{sel_year}-01", f"{sel_year}-12"))
                this_year_mean = this_year_ds.mean(dim=['lat', 'lon']) * info["scale"]
                m_df = this_year_mean.to_dataframe().reset_index()
                m_df['Month'] = pd.to_datetime(m_df['time']).dt.strftime('%b')
                
                fig_month = px.bar(m_df, x='Month', y=var,
                                   title=f"Monthly Cycle in {sel_year}",
                                   labels={var: unit},
                                   color_discrete_sequence=['#38bdf8'])
                fig_month.update_layout(
                    height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.2)',
                    font=dict(family='Space Grotesk', color='#e2e8f0'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.05)'), 
                    yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                st.plotly_chart(fig_month, use_container_width=True, theme=None)
            except Exception as e:
                st.error(f"Could not render monthly cycle: {e}")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Time Series from Repo_1 (point-based) ---
        st.markdown("<h3 style='color: #f8fafc;'>📍 Location-based Time Series</h3>", unsafe_allow_html=True)
        
        with st.container(border=True):
            ts_c1, ts_c2 = st.columns(2)
            try:
                lat_p = ts_c1.number_input("Latitude", value=float(ds_3d.lat.mean()), key="analysis_lat")
                lon_p = ts_c2.number_input("Longitude", value=float(ds_3d.lon.mean()), key="analysis_lon")
            except Exception:
                lat_p = ts_c1.number_input("Latitude", value=20.0, key="analysis_lat")
                lon_p = ts_c2.number_input("Longitude", value=78.0, key="analysis_lon")

        try:
            fig_ts = create_timeseries(ds_3d, repo1_var, lat_p, lon_p)
            fig_ts.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.2)',
                font=dict(family='Space Grotesk', color='#e2e8f0'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', title_font=dict(color='#e2e8f0')),
                yaxis=dict(gridcolor='rgba(255,255,255,0.05)', title_font=dict(color='#e2e8f0')),
                height=450
            )
            fig_ts.update_traces(line=dict(width=2, color="#38bdf8"))
            st.plotly_chart(fig_ts, use_container_width=True, theme=None)
        except Exception as e:
            st.error(f"Could not render time series: {e}")

    # ═══════════════════════════════════════════════════════════════════
    # TAB 2 — COMPARISON (from Repo_2 Dataset Comparison)
    # ═══════════════════════════════════════════════════════════════════
    elif selected_tab == "📊 Comparison":
        st.markdown("<h1 style='color: #f8fafc;'>Dataset <span style='color: #38bdf8;'>Comparison</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Annual global mean for all three variables plotted together (normalised to z-scores for comparability).</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # --- All-Dataset Annual Mean Comparison ---
        colors = {'Air Temperature (NCEP)': '#ef4444',
                  'Wind Speed U-component': '#38bdf8',
                  'Precipitation Rate':     '#10b981'}

        fig_compare = go.Figure()
        for dname, dinfo in DATASETS.items():
            d, s  = all_ds[dname]
            v     = dinfo["var"]
            ann   = annual_mean_timeseries(d, v)
            val   = ann[v] * s
            zscore = (val - val.mean()) / val.std()
            fig_compare.add_trace(go.Scatter(
                x=ann['year'], y=zscore, mode='lines',
                name=dname,
                line=dict(color=colors[dname], width=2)
            ))

        fig_compare.add_hline(y=0, line_color='rgba(255,255,255,0.2)', line_dash='dot')
        fig_compare.update_layout(
            height=480,
            title="Normalised Annual Global Mean — Temperature vs Wind vs Precipitation (1948–2026)",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.2)',
            font=dict(family='Space Grotesk', color='#e2e8f0'),
            xaxis=dict(title='Year', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='Z-score (std deviations from mean)', gridcolor='rgba(255,255,255,0.05)'),
            legend=dict(
                bgcolor='rgba(0,0,0,0.3)', bordercolor='rgba(255,255,255,0.1)', borderwidth=1,
                font=dict(color='#e2e8f0')
            )
        )
        st.plotly_chart(fig_compare, use_container_width=True, theme=None)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Correlation Matrix ---
        st.markdown("<h2 style='color: #f8fafc;'>📐 Correlation <span style='color: #10b981;'>Matrix</span></h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8;'>Pearson correlation between the annual global means of all loaded datasets.</p>", unsafe_allow_html=True)
        
        combined = {}
        for dname, dinfo in DATASETS.items():
            d, s   = all_ds[dname]
            v   = dinfo["var"]
            ann = annual_mean_timeseries(d, v)
            combined[dname] = ann[v].values * s

        min_len = min(len(v) for v in combined.values())
        corr_df = pd.DataFrame({k: v[:min_len] for k, v in combined.items()}).corr().round(3)
        
        fig_corr = px.imshow(corr_df,
                             text_auto=True,
                             aspect="auto",
                             color_continuous_scale='RdYlGn',
                             range_color=[-1, 1],
                             labels=dict(color="Correlation"),
                             title="Correlation between Temperature, Wind, and Precipitation")
        
        fig_corr.update_layout(
            height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.2)',
            font=dict(family='Space Grotesk', color='#e2e8f0')
        )
        st.plotly_chart(fig_corr, use_container_width=True, theme=None)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Side-by-Side Year Comparison ---
        st.markdown("<h2 style='color: #f8fafc;'>🔀 Side-by-Side <span style='color: #38bdf8;'>Year Comparison</span></h2>", unsafe_allow_html=True)
        
        with st.container(border=True):
            comp_c1, comp_c2, comp_c3 = st.columns(3)
            comp_dataset = comp_c1.selectbox("Dataset for comparison", list(DATASETS.keys()), key="comp_ds")
            comp_info = DATASETS[comp_dataset]
            comp_ds, comp_scale = all_ds[comp_dataset]
            comp_var = comp_info["var"]
            comp_unit = comp_info["unit"]
            
            comp_times = pd.DatetimeIndex(comp_ds['time'].values)
            comp_years = sorted(comp_times.year.unique())
            
            yr_left = comp_c2.slider("Year A", int(comp_years[0]), int(comp_years[-1]), 1990, key="yr_a")
            yr_right = comp_c3.slider("Year B", int(comp_years[0]), int(comp_years[-1]), 2020, key="yr_b")

        col_left, col_right = st.columns(2)

        def year_map(yr, mo=6):
            sliced = get_slice(comp_ds, comp_var, yr, mo, comp_scale)
            df = slice_to_df(sliced, comp_var)
            vmin = float(df[comp_var].quantile(0.02))
            vmax = float(df[comp_var].quantile(0.98))
            f = px.scatter_geo(df, lat='lat', lon='lon', color=comp_var,
                              color_continuous_scale='RdBu_r',
                              range_color=[vmin, vmax],
                              projection='natural earth',
                              title=f"{comp_dataset} — {yr} (June)",
                              labels={comp_var: comp_unit},
                              hover_data={'lat': ':.1f', 'lon': ':.1f', comp_var: ':.2f'})
            f.update_traces(marker=dict(size=3, opacity=0.7))
            f.update_layout(
                height=400, paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Space Grotesk', color='#e2e8f0'),
                margin=dict(l=0, r=0, t=40, b=0),
                geo=dict(bgcolor='rgba(0,0,0,0)', showocean=True, oceancolor='#0c4a6e',
                         showland=True, landcolor='#1e3a5f',
                         showcoastlines=True, coastlinecolor='#38bdf8', showframe=False)
            )
            return f

        # Initialize session state for comparison figures and years
        if "prev_yr_a" not in st.session_state:
            st.session_state.prev_yr_a = None
        if "prev_yr_b" not in st.session_state:
            st.session_state.prev_yr_b = None
        if "fig_left" not in st.session_state:
            st.session_state.fig_left = None
        if "fig_right" not in st.session_state:
            st.session_state.fig_right = None
        if "prev_comp_dataset" not in st.session_state:
            st.session_state.prev_comp_dataset = None

        # Reset session state if the comparison dataset changes
        if st.session_state.prev_comp_dataset != comp_dataset:
            st.session_state.prev_comp_dataset = comp_dataset
            st.session_state.prev_yr_a = None
            st.session_state.prev_yr_b = None
            st.session_state.fig_left = None
            st.session_state.fig_right = None

        # Update fig_left only if yr_left changed (or not computed yet)
        if st.session_state.prev_yr_a != yr_left or st.session_state.fig_left is None:
            st.session_state.fig_left = year_map(yr_left)
            st.session_state.prev_yr_a = yr_left

        # Update fig_right only if yr_right changed (or not computed yet)
        if st.session_state.prev_yr_b != yr_right or st.session_state.fig_right is None:
            st.session_state.fig_right = year_map(yr_right)
            st.session_state.prev_yr_b = yr_right

        with col_left:
            st.plotly_chart(st.session_state.fig_left, use_container_width=True, theme=None)
        with col_right:
            st.plotly_chart(st.session_state.fig_right, use_container_width=True, theme=None)

        # Difference map
        st.markdown("<h3 style='color: #f8fafc;'>Difference Map (Year B − Year A)</h3>", unsafe_allow_html=True)
        try:
            left_arr = get_slice(comp_ds, comp_var, yr_left, 6, comp_scale)
            right_arr = get_slice(comp_ds, comp_var, yr_right, 6, comp_scale)
            diff_arr = right_arr - left_arr
            df_diff = diff_arr.to_dataframe(name='diff').reset_index().dropna(subset=['diff'])

            fig_diff = px.scatter_geo(df_diff, lat='lat', lon='lon', color='diff',
                                       color_continuous_scale='RdBu_r', range_color=[-5, 5],
                                       projection='natural earth',
                                       title=f"Change: {yr_right} minus {yr_left}  ({comp_unit})",
                                       labels={'diff': f'Δ {comp_unit}'},
                                       hover_data={'lat': ':.1f', 'lon': ':.1f', 'diff': ':.2f'})
            fig_diff.update_traces(marker=dict(size=3, opacity=0.7))
            fig_diff.update_layout(
                height=430, paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Space Grotesk', color='#e2e8f0'),
                geo=dict(bgcolor='rgba(0,0,0,0)', showocean=True, oceancolor='#0c4a6e',
                         showland=True, landcolor='#1e3a5f',
                         showcoastlines=True, coastlinecolor='#38bdf8', showframe=False)
            )
            st.plotly_chart(fig_diff, use_container_width=True, theme=None)

            # Summary stats
            mean_diff = float(df_diff['diff'].mean())
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Mean change", f"{mean_diff:+.2f} {comp_unit}")
            sc2.metric("Max warming region", f"{df_diff['diff'].max():+.2f} {comp_unit}")
            sc3.metric("Max cooling region", f"{df_diff['diff'].min():+.2f} {comp_unit}")
        except Exception as e:
            st.error(f"Could not render difference map: {e}")

    # ═══════════════════════════════════════════════════════════════════
    # TAB 3 — TIME STORY (Video playback)
    # ═══════════════════════════════════════════════════════════════════
    elif selected_tab == "🎬 Time Story":
        st.markdown("<h1 style='color: #f8fafc;'>Climate <span style='color: #f59e0b;'>Time Story</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>Watch the evolution of our planet's climate unfold over decades — a visual narrative of change.</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "time_story.mp4")
        
        if os.path.exists(video_path):
            # Read video file and encode to base64 for HTML embedding
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
            
            video_b64 = base64.b64encode(video_bytes).decode()
            
            # Full-width cinematic video player without controls for direct playing
            st.markdown(f"""
                <div style="
                    position: relative; 
                    border-radius: 16px; 
                    overflow: hidden; 
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                    border: 1px solid rgba(56, 189, 248, 0.2);
                ">
                    <video 
                        autoplay 
                        loop 
                        muted 
                        playsinline
                        style="
                            width: 100%; 
                            display: block; 
                            border-radius: 16px;
                        "
                    >
                        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Info cards below the video
            info_c1, info_c2, info_c3 = st.columns(3)
            with info_c1:
                st.markdown("""
                    <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; text-align: center;">
                        <h3 style="color: #38bdf8; margin-bottom: 8px;">📅 Timeline</h3>
                        <p style="color: #94a3b8; margin: 0;">Decades of climate data compressed into a visual narrative</p>
                    </div>
                """, unsafe_allow_html=True)
            with info_c2:
                st.markdown("""
                    <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; text-align: center;">
                        <h3 style="color: #10b981; margin-bottom: 8px;">🌡️ Variables</h3>
                        <p style="color: #94a3b8; margin: 0;">Temperature, Precipitation & Wind patterns evolving over time</p>
                    </div>
                """, unsafe_allow_html=True)
            with info_c3:
                st.markdown("""
                    <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; text-align: center;">
                        <h3 style="color: #f59e0b; margin-bottom: 8px;">🎯 Impact</h3>
                        <p style="color: #94a3b8; margin: 0;">See how global warming accelerates across continents</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Video file not found. Please ensure the video file is present in the Final folder.")
            st.info(f"Expected path: {video_path}")
