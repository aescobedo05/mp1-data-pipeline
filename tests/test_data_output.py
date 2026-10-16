#tests/test_data_output.py

import pandas as pd

from src import save_data


def test_save_data_creates_csv(sample_df, tmp_path):
    output_path = tmp_path / "clean.csv"

    results = save_data(sample_df, output_path)

    df = pd.read_csv(results)

    assert results == output_path
    assert len(df) == len(sample_df)
    assert df.columns.equals(sample_df.columns)

