 
import xarray as xr
import pandas as pd
import os

DATA_DIR = "data"


def load_temperature(time_index):

    ds = xr.open_dataset(os.path.join(DATA_DIR,"air.mon.mean.nc"))
    ds = ds.rename({"air":"temperature"})

    data = ds["temperature"].isel(time=time_index)

    df = data.to_dataframe().reset_index()

    df["temperature"] = df["temperature"]

    df = df.rename(columns={"lat":"latitude","lon":"longitude"})

    return ds, df


def load_precipitation(time_index):

    ds = xr.open_dataset(os.path.join(DATA_DIR,"sample_data.nc"))
    ds = ds.rename({"prate":"precipitation"})

    data = ds["precipitation"].isel(time=time_index)

    df = data.to_dataframe().reset_index()

    df = df.rename(columns={"lat":"latitude","lon":"longitude"})

    return ds, df


def load_pressure(time_index):

    ds = xr.open_dataset(os.path.join(DATA_DIR,"uwnd.mon.mean.nc"))
    ds = ds.rename({"uwnd":"pressure"})

    data = ds["pressure"].isel(time=time_index)

    df = data.to_dataframe().reset_index()

    df = df.rename(columns={"lat":"latitude","lon":"longitude"})

    return ds, df