#tests/test_data_processor.py

import pandas as pd
import pytest

from src.data_processor import handle_missing, remove_duplicates, remove_outliers


def test_remove_duplicates(sample_df):
    results = remove_duplicates(sample_df)

    assert len(results) == 98



def test_handle_missing_rows(sample_df):
    # Arrange: use the existing rating column.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    # note: errors="coerce" converts invalid numeric strings to missing values.

    results = handle_missing(df, axis="rows")

    assert len(results) == 97


def test_remove_outliers_iqr(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna()
    # note: errors="coerce" converts invalid numeric strings to missing values.

    results = remove_outliers(df, ["rating"], method="iqr", threshold=1.5)

    assert len(results) == 95

def test_remove_outliers_zscore(sample_df):
    # Arrange: use numeric ratings and exclude missing values.
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna()
    # note: errors="coerce" converts invalid numeric strings to missing values.

    results = remove_outliers(df, ["rating"], method="zscore", threshold=3)

    assert len(results) == 95

def test_remove_outliers_with_unsupported_method(sample_df):
    df = sample_df[["rating"]].copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna()

    with pytest.raises(ValueError):
        remove_outliers(df, ["rating"], method="unkown", threshold=3)
