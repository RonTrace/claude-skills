#!/usr/bin/env python3
"""
Output Formatting Utilities for CLI Tools

Provides consistent output formatting for console, CSV, and JSON.

Usage:
    from output_utils import print_table, export_to_csv, export_to_json

    # Console table
    print_table(['Name', 'Email'], [['Alice', 'alice@example.com'], ['Bob', 'bob@example.com']])

    # CSV export
    export_to_csv('output.csv', ['Name', 'Email'], data)

    # JSON export
    export_to_json('output.json', {'users': data})
"""

import csv
import json
import sys
from datetime import datetime
from typing import List, Any, Dict, Optional


def format_number(n: int) -> str:
    """
    Format number with commas.

    Args:
        n: Integer to format

    Returns:
        Formatted string like "1,234,567"
    """
    return f"{n:,}"


def format_percent(n: int, total: int, decimals: int = 1) -> str:
    """
    Format as percentage.

    Args:
        n: Numerator
        total: Denominator
        decimals: Decimal places

    Returns:
        Formatted string like "25.0%" or "N/A" if total is 0
    """
    if total == 0:
        return "N/A"
    return f"{n / total * 100:.{decimals}f}%"


def format_duration(seconds: float) -> str:
    """
    Format seconds as human-readable duration.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string like "1.5s", "2.5m", or "1.2h"
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds / 60:.1f}m"
    else:
        return f"{seconds / 3600:.1f}h"


def print_table(headers: List[str], rows: List[List[Any]], min_width: int = 10) -> None:
    """
    Print a formatted ASCII table to stdout.

    Args:
        headers: List of column header strings
        rows: List of row data (each row is a list of values)
        min_width: Minimum column width
    """
    if not rows:
        print("(no data)")
        return

    # Calculate column widths
    widths = [max(min_width, len(str(h))) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))

    # Print header
    header_line = ' | '.join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print('-' * len(header_line))

    # Print rows
    for row in rows:
        row_line = ' | '.join(
            str(cell).ljust(widths[i]) if i < len(widths) else str(cell)
            for i, cell in enumerate(row)
        )
        print(row_line)


def print_dict_table(data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> None:
    """
    Print a table from a list of dictionaries.

    Args:
        data: List of dictionaries (rows)
        columns: Optional list of column names to include (defaults to all keys)
    """
    if not data:
        print("(no data)")
        return

    if columns is None:
        columns = list(data[0].keys())

    rows = [[row.get(col, '') for col in columns] for row in data]
    print_table(columns, rows)


class DateTimeEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime objects."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def export_to_csv(filename: str, headers: List[str], rows: List[List[Any]]) -> None:
    """
    Export data to CSV file.

    Args:
        filename: Output file path
        headers: List of column headers
        rows: List of row data
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Exported {len(rows)} rows to {filename}")


def export_dicts_to_csv(filename: str, data: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> None:
    """
    Export list of dictionaries to CSV.

    Args:
        filename: Output file path
        data: List of dictionaries
        columns: Optional list of column names (defaults to all keys from first row)
    """
    if not data:
        print("No data to export")
        return

    if columns is None:
        columns = list(data[0].keys())

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
    print(f"Exported {len(data)} rows to {filename}")


def export_to_json(filename: str, data: Any, indent: int = 2) -> None:
    """
    Export data to JSON file.

    Args:
        filename: Output file path
        data: Data to export (dict, list, etc.)
        indent: Indentation level for pretty printing
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, cls=DateTimeEncoder)
    print(f"Exported to {filename}")


def error_exit(message: str, code: int = 1) -> None:
    """
    Print error message to stderr and exit.

    Args:
        message: Error message
        code: Exit code (default 1)
    """
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(code)


def print_summary(title: str, items: Dict[str, Any]) -> None:
    """
    Print a formatted summary section.

    Args:
        title: Section title
        items: Dictionary of label -> value pairs
    """
    print(f"\n{title}")
    print("=" * len(title))
    max_label_len = max(len(str(k)) for k in items.keys())
    for label, value in items.items():
        print(f"  {label:<{max_label_len}} : {value}")


if __name__ == "__main__":
    # Demo output utilities
    print("Output Utilities Demo")
    print("=" * 50)

    # Table demo
    print("\nTable Demo:")
    headers = ['Name', 'Email', 'Count']
    rows = [
        ['Alice', 'alice@example.com', 42],
        ['Bob', 'bob@example.com', 17],
        ['Charlie', 'charlie@example.com', 99],
    ]
    print_table(headers, rows)

    # Formatting demos
    print("\nFormatting Demo:")
    print(f"  format_number(1234567) = {format_number(1234567)}")
    print(f"  format_percent(25, 100) = {format_percent(25, 100)}")
    print(f"  format_duration(3661) = {format_duration(3661)}")

    # Summary demo
    print_summary("Analysis Summary", {
        'Total Users': format_number(12345),
        'Active Rate': format_percent(8765, 12345),
        'Processing Time': format_duration(45.7),
    })
