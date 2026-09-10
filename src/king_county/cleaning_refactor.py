import pandas as pd

def clean_data(df:pd.DataFrame) -> pd.DataFrame:

    # Drop the implausible row.
    df = df.drop(15856, axis=0)

    # Recalculate `sqft_basement` as `sqft_living - sqft_above`.
    df["sqft_basement"] = df["sqft_living"] - df["sqft_above"]

    # Replace missing values in `view` with the most frequent value (0).
    df["view"] = df["view"].fillna(0)

    # Replace missing values in `waterfront` with the most frequent value (0).
    df["waterfront"] = df["waterfront"].fillna(0)

    # Create an empty list to store the derived values.
    last_known_change = []

    # Inspect the `yr_renovated` value for each row.
    for idx, yr_re in df["yr_renovated"].items():
        # If `yr_renovated` is 0 or missing, use the original build year instead.
        if str(yr_re) == "nan" or yr_re == 0.0:
            last_known_change.append(df["yr_built"][idx])
        # Otherwise, keep the renovation year in the new list.
        else:
            last_known_change.append(int(yr_re))

    # Create a new column from the values collected above.
    df["last_known_change"] = last_known_change

    # Drop the original `yr_renovated` and `yr_built` columns.
    df = df.drop("yr_renovated", axis=1)
    df = df.drop("yr_built", axis=1)

    return df