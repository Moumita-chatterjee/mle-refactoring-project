import numpy as np
import pandas as pd

# This helper function calculates the distance between one house and a reference location.
def dist(long, lat, ref_long, ref_lat):
    """dist computes the distance in km to a reference location.
    Input: long and lat of the location of interest and ref_long and ref_lat
    as the long and lat of the reference location"""
    delta_long = long - ref_long
    delta_lat = lat - ref_lat
    delta_long_corr = delta_long * np.cos(np.radians(ref_lat))
    return (
        ((delta_long_corr) ** 2 + (delta_lat) ** 2) ** (1 / 2) * 2 * np.pi * 6378 / 360
    )


def feature_data(df: pd.DataFrame) -> pd.DataFrame:
    df["sqft_price"] = (
    df.price / (df.sqft_living + df.sqft_lot)).round(2)
    # Absolute difference in latitude between the center and the property.
    df["delta_lat"] = np.absolute(47.62774 - df["lat"])
    # Absolute difference in longitude between the center and the property.
    df["delta_long"] = np.absolute(-122.24194 - df["long"])
    # Distance between the center and the property.
    df["center_distance"] = dist(df["long"], df["lat"], -122.24194, 47.62774)

    # All waterfront houses, used as reference points.
    water_list = df.query("waterfront == 1")
    water_distance = []
    # For each row, calculate the distance to the nearest waterfront house.
    for idx in df.index:
        ref_list = []
        for x, y in zip(list(water_list["long"]), list(water_list["lat"])):
            ref_list.append(dist(df["long"][idx], df["lat"][idx], x, y).min())
        water_distance.append(min(ref_list))

    df["water_distance"] = water_distance

    return df