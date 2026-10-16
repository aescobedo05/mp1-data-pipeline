# tests/test_data_validator.py

import pytest

from src import validate_dataframe


def test_validate_dataframe_removes_invalid_ratings(sample_df):
    required_columns = {"record_id", "name", "rating", "category", "status"}
    numeric_columns = {"record_id", "rating"}

    results = validate_dataframe(sample_df, required_columns, numeric_columns)

    assert list(results.columns) == ["record_id", "name", "rating", "category", "status"]
    assert len(results) == 98


def test_validate_dataframe_with_missing_column(sample_df):
    required_columns = {"record_id", "name", "rating", "category", "status", "gross_income"}
    numeric_columns = {"record_id", "rating"}

    with pytest.raises(ValueError):
        validate_dataframe(sample_df, required_columns, numeric_columns)
