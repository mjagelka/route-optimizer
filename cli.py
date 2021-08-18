#!/usr/bin/env python3

import argparse
import logging

from processor import Processor

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger()


def main() -> None:
    """Run the workflow."""
    parser = create_parser()
    args = parser.parse_args()

    if args.debug:
        LOG.setLevel(logging.DEBUG)

    if args.precision is None:
        processor = Processor(args.json)
    elif args.precision == 0:
        processor = Processor(args.json, None)
    else:
        processor = Processor(args.json, args.precision)
    processor.minimize()


def create_parser() -> argparse.ArgumentParser:
    """Create an argument parser."""
    parser = argparse.ArgumentParser(
        description='Tool for calculating the optimal route between cities')
    parser.add_argument(
        '--json', required=True, help='Absolute or relative path to the json '
                                      'file containing cities GPS coordinates')
    parser.add_argument(
        '--precision', type=int, help='Number of decimals used for rounding')
    parser.add_argument(
        '--debug', action='store_true', help='Show debug logging')
    return parser


if __name__ == "__main__":
    main()
