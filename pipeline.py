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
from pathlib import Path

from data_loaders import load_data
from data_processor import process_data, create_cleaning_report


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    if verbose is True:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
            datefmt="%H:%M:%S"
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
            datefmt="%H:%M:%S"
                )



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


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file() is True:
        logger.info("Input file validated: %s", filepath)
        return True
    else:
        logger.error("Input file not found: %s", filepath)
        sys.exit(1)


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

    try:
        df = process_data(df, config)
    except ValueError:
        sys.exit(1)

    logger.info("Processing complete: %s -> %s rows", len(original_df), len(df))

    report = create_cleaning_report(original_df, df)
    print(report)

    logger.info("Saved clean data to %s", args.output)



if __name__ == "__main__":
    main()
