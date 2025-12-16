import pandas as pd

def load_catalogue(path="data/shl_product_catalogue.csv"):
    df = pd.read_csv(path)
    df.fillna("", inplace=True)
    return df
