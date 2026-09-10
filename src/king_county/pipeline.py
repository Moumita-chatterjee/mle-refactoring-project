from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


from .cleaning_refactor import clean_data
from .features_refactor import feature_data

cleaning_feature_pipeline = Pipeline(steps=[
    ("cleaning", FunctionTransformer(clean_data)),
    ("featuring", FunctionTransformer(feature_data))
])




if __name__ == "__main__":
    import pandas as pd

    data_path = Path(__file__).resolve().parents[2] / "data" / "King_County_House_prices_dataset.csv"
    df = pd.read_csv(data_path)
    result = cleaning_feature_pipeline.fit_transform(df)
    print(result.shape)
    print(result.head())