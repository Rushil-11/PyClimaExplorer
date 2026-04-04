import streamlit as st
import pandas as pd

from modules.data_loader import (
    load_temperature,
    load_precipitation,
    load_pressure
)

from modules.visualization import (
    create_globe,
    create_timeseries
)


st.set_page_config(page_title="PyClimaExplorer",layout="wide")

st.markdown("""
<style>

[data-testid="stSidebar"] {display:none;}

.main {
background-color: white;
color: blue;
}

</style>
""", unsafe_allow_html=True)


col1,col2 = st.columns([4,1])

with col1:
    st.title("🌍 PyClimaExplorer")

with col2:

    variable_choice = st.selectbox(
        "Climate Variable",
        ["Temperature","Precipitation","Pressure"]
    )


# LOAD DATASET FIRST TO GET TIME RANGE

if variable_choice=="Temperature":

    temp_ds,_ = load_temperature(0)
    ds = temp_ds
    variable="temperature"

elif variable_choice=="Precipitation":

    temp_ds,_ = load_precipitation(0)
    ds = temp_ds
    variable="precipitation"

else:

    temp_ds,_ = load_pressure(0)
    ds = temp_ds
    variable="pressure"


# TIMELINE SLIDER
time_index = st.slider(
    "Timeline(Look below for the Date)",
    0,
    len(ds.time)-1,
    0
)

st.write(
    "Data showing for:",
    pd.to_datetime(ds.time.values[time_index])
)


# LOAD DATA AGAIN WITH SELECTED TIME
if variable=="temperature":

    ds,df = load_temperature(time_index)

elif variable=="precipitation":

    ds,df = load_precipitation(time_index)

else:

    ds,df = load_pressure(time_index)


# GLOBE
fig = create_globe(df,variable)

st.plotly_chart(fig,use_container_width=True)


# TIME SERIES
st.divider()

st.subheader(f"{variable_choice} Trend Analysis")

c1,c2 = st.columns(2)

with c1:
    lat_p = st.number_input(
        "Latitude",
        value=float(ds.lat.mean())
    )

with c2:
    lon_p = st.number_input(
        "Longitude",
        value=float(ds.lon.mean())
    )


fig_ts = create_timeseries(
    ds,
    variable,
    lat_p,
    lon_p
)

st.plotly_chart(fig_ts,use_container_width=True)