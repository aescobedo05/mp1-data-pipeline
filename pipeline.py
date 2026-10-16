"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check the quality of a CSV file."
        )

    parser.add_argument("--input", "-i",
                        required=True,
                        help="Path to the input file"
                        )

    parser.add_argument("--config",
                        required=True,
                        help="Configuration file"
                        )

    parser.add_argument("--output", "-o",
                        required=True,
                        help="Path to the output file"
                        )

    parser.add_argument("--verbose", "-v",
                        action="store_true",
                        help="Enable verbose logging"
                        )

    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()

    setup_logging(args.verbose)

    logger.debug("Arguments parsed: input=%s, config=%s, output=%s",
                 args.input, args.config, args.output)

    validate_input(args.input)
    validate_input(args.config)

    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    original_df = df.copy()

    validation = config["validation"]

    require_cols = validation["required_columns"]
    nume_cols = validation["numeric_columns"]

    try:
        validated_df = validate_dataframe(df, require_cols, nume_cols)
    except ValueError:
        sys.exit(1)

    logger.info("rows before validation:%s, rows after: %s", len(original_df), len(validated_df))

    try:
        df = process_data(validated_df, config)
    except ValueError:
        sys.exit(1)

    logger.info("Processing complete: %s -> %s rows", len(validated_df), len(df))

    report = create_cleaning_report(original_df, df)

    save_data(df, args.output)
    logger.info("Saved clean data to %s", args.output)

    print(report)




if __name__ == "__main__":
    main()
