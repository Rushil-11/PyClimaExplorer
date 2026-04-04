
import plotly.graph_objects as go
import pandas as pd


def create_globe(df,variable):

    if variable=="temperature":

        colorscale="Turbo"
        color_title="Temperature (°C)"

    elif variable=="precipitation":

        colorscale="Twilight"
        color_title="Precipitation (meter)"

    else:

        colorscale="Balance"
        color_title="Pressure (kPa)"


    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(

            lon=df["longitude"],
            lat=df["latitude"],
            mode="markers",

            marker=dict(
                size=12,
                opacity=0.6,
                color=df[variable],
                colorscale=colorscale,
                showscale=True,
                colorbar_title=color_title
            )
        )
    )

    fig.update_layout(

        geo=dict(
            projection_type="orthographic",

            showland=True,
            landcolor="rgb(52,165,111)",

            showocean=True,
            oceancolor="rgb(0,103,146)"
        ),

        height=650,
        margin=dict(l=0,r=0,t=0,b=0)
    )

    return fig



def create_timeseries(ds,variable,lat_p,lon_p):

    ts = ds[variable].sel(lat=lat_p,lon=lon_p,method="nearest")

    values = ts.values

    if variable=="temperature":
        values = values

    time_vals = pd.to_datetime(ds.time.values)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time_vals,
            y=values,
            mode="lines",
            line=dict(width=3,color="orange")
        )
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title=variable,
        height=650
    )

    return fig