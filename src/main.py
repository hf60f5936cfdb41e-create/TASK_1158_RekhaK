#!/usr/bin/env python3
"""
CLI application for processing customer data with filtering capabilities.
"""
import argparse
import csv
import json
import sys
from typing import List, Dict, Any


def load_customers(input_path: str) -> List[Dict[str, Any]]:
    """Load customer data from CSV file."""
    customers = []
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                customers.append(row)
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    return customers


def filter_customers(customers: List[Dict[str, Any]],
                     country: str = None,
                     min_age: int = None) -> List[Dict[str, Any]]:
    """Filter customers based on country and minimum age."""
    filtered = customers

    if country:
        filtered = [c for c in filtered if c.get('country') == country]

    if min_age is not None:
        filtered = [c for c in filtered
                    if c.get('age') and int(c.get('age')) >= min_age]

    return filtered


def save_results(output_path: str, data: List[Dict[str, Any]]) -> None:
    """Save filtered results to JSON file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


def process_command(args: argparse.Namespace) -> None:
    """Execute the process command."""
    # Load customers
    customers = load_customers(args.input)
    print(f"Loaded {len(customers)} customers from {args.input}")

    # Filter customers
    filtered = filter_customers(customers, args.country, args.min_age)
    print(f"Filtered to {len(filtered)} customers", end="")

    filters = []
    if args.country:
        filters.append(f"country={args.country}")
    if args.min_age:
        filters.append(f"min_age={args.min_age}")

    if filters:
        print(f" ({', '.join(filters)})")
    else:
        print()

    # Save results
    save_results(args.output, filtered)
    print(f"Results saved to {args.output}")


def main():
    """Main entry point for the CLI application."""
    parser = argparse.ArgumentParser(
        description='CLI application for processing customer data'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Process command
    process_parser = subparsers.add_parser(
        'process',
        help='Process customer data with optional filtering'
    )
    process_parser.add_argument(
        '--input',
        required=True,
        help='Input CSV file path'
    )
    process_parser.add_argument(
        '--output',
        required=True,
        help='Output JSON file path'
    )
    process_parser.add_argument(
        '--country',
        help='Filter by country'
    )
    process_parser.add_argument(
        '--min-age',
        type=int,
        help='Filter by minimum age'
    )

    args = parser.parse_args()

    if args.command == 'process':
        process_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
