## MP1 end-to-end pipeline
This pipeline loads raw messy data, validates, cleans, and then saves the data using configurable settings. `pipeline.py` is the pipeline function, you call this module to initiate the data pipeline process. First `utils.py` sets up logging and validates the inputted file to ensure it exists. `data_loaders.py` loads the messy data depending on filetype, then `data_validator.py` validates the dataframe using the configurations in the config file. `data_processor.py` processes adn cleans the data, and finally `data_output.py` saves the cleaned dataframe as a new csv file. All of the components of the pipeline are stored in `src/`, the configuration file is stored in `config/`, messy data files are stored in `fixtures/`, and the outputted clean data is saved in `output/`.

### Example Command
```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

### Results
```text
10:24:50 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
10:24:50 INFO     src.utils — Input file validated: fixtures/sample_data.csv
10:24:50 INFO     src.utils — Input file validated: config/config.yaml
10:24:50 INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
10:24:50 INFO     src.data_loaders — Loaded YAML file: config\config.yaml
10:24:50 WARNING  src.data_validator — not_available is an invaild numeric value
10:24:50 WARNING  src.data_validator — error is an invaild numeric value
10:24:50 DEBUG    src.data_validator — 98 valid rows, 2 rows removed
10:24:50 INFO     __main__ — rows before validation:100, rows after: 98
10:24:50 DEBUG    src.data_processor — Row count after removing duplicates: 96
10:24:50 DEBUG    src.data_processor — Row count after dropping rows with missing values: 94
10:24:50 DEBUG    src.data_processor — method: iqr, threshold: 1.5, 2 rows removed
10:24:50 INFO     __main__ — Processing complete: 100 -> 92 rows
10:24:50 DEBUG    src.data_output — rows saved: 92, output file: output/clean.csv
10:24:50 INFO     __main__ — Saved clean data to output/clean.csv
{'row_before': 100, 'rows_after': 92, 'rows_removed': 8, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```