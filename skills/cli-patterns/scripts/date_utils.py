#!/usr/bin/env python3
"""
Date Parsing Utilities for CLI Tools

Provides flexible date parsing for CLI arguments.
Supports relative dates (7d, 2w, 1m) and absolute dates (YYYY-MM-DD).

Usage:
    from date_utils import parse_relative_date, get_date_range

    start = parse_relative_date('7d')     # 7 days ago
    start = parse_relative_date('2w')     # 2 weeks ago
    start = parse_relative_date('1m')     # ~30 days ago
    start = parse_relative_date('today')  # Start of today
    start = parse_relative_date('2025-01-15')  # Specific date

    start, end = get_date_range('7d', 'today')
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional


def parse_relative_date(date_str: str) -> datetime:
    """
    Parse relative or absolute date string.

    Args:
        date_str: One of:
            - 'today' - Start of today (midnight)
            - 'yesterday' - Start of yesterday
            - '7d' - 7 days ago
            - '2w' - 2 weeks ago
            - '1m' - ~1 month ago (30 days)
            - '3m' - ~3 months ago (90 days)
            - '1y' - ~1 year ago (365 days)
            - 'YYYY-MM-DD' - Specific date

    Returns:
        datetime object

    Raises:
        ValueError: If date string format is not recognized
    """
    date_str = date_str.lower().strip()

    # Named dates
    if date_str == 'today':
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_str == 'yesterday':
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    elif date_str == 'now':
        return datetime.now()

    # Relative dates
    if date_str.endswith('d'):
        try:
            days = int(date_str[:-1])
            return datetime.now() - timedelta(days=days)
        except ValueError:
            pass

    if date_str.endswith('w'):
        try:
            weeks = int(date_str[:-1])
            return datetime.now() - timedelta(weeks=weeks)
        except ValueError:
            pass

    if date_str.endswith('m'):
        try:
            months = int(date_str[:-1])
            return datetime.now() - timedelta(days=months * 30)  # Approximate
        except ValueError:
            pass

    if date_str.endswith('y'):
        try:
            years = int(date_str[:-1])
            return datetime.now() - timedelta(days=years * 365)  # Approximate
        except ValueError:
            pass

    # Absolute date formats
    date_formats = [
        '%Y-%m-%d',           # 2025-01-15
        '%Y/%m/%d',           # 2025/01/15
        '%m/%d/%Y',           # 01/15/2025
        '%d-%m-%Y',           # 15-01-2025
        '%Y-%m-%d %H:%M:%S',  # 2025-01-15 14:30:00
    ]

    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    raise ValueError(
        f"Unrecognized date format: '{date_str}'. "
        f"Expected: 7d, 2w, 1m, today, yesterday, or YYYY-MM-DD"
    )


def get_date_range(start_str: str, end_str: Optional[str] = None) -> Tuple[datetime, datetime]:
    """
    Get start and end dates from strings.

    Args:
        start_str: Start date string (see parse_relative_date)
        end_str: End date string, defaults to now if not provided

    Returns:
        Tuple of (start_date, end_date)
    """
    start = parse_relative_date(start_str)
    end = parse_relative_date(end_str) if end_str else datetime.now()
    return start, end


def format_date(dt: datetime, fmt: str = '%Y-%m-%d') -> str:
    """
    Format datetime for display.

    Args:
        dt: datetime object
        fmt: strftime format string

    Returns:
        Formatted date string
    """
    return dt.strftime(fmt)


def format_date_range(start: datetime, end: datetime) -> str:
    """
    Format a date range for display.

    Args:
        start: Start datetime
        end: End datetime

    Returns:
        Formatted string like "2025-01-01 to 2025-01-15"
    """
    return f"{format_date(start)} to {format_date(end)}"


def days_between(start: datetime, end: datetime) -> int:
    """
    Calculate number of days between two dates.

    Args:
        start: Start datetime
        end: End datetime

    Returns:
        Number of days (can be negative if end < start)
    """
    return (end - start).days


if __name__ == "__main__":
    # Demo date parsing
    test_cases = [
        'today',
        'yesterday',
        '7d',
        '2w',
        '1m',
        '3m',
        '2025-01-15',
    ]

    print("Date Parsing Demo:")
    print("-" * 50)
    for case in test_cases:
        try:
            result = parse_relative_date(case)
            print(f"  '{case}' → {format_date(result, '%Y-%m-%d %H:%M')}")
        except ValueError as e:
            print(f"  '{case}' → ERROR: {e}")

    print("\nDate Range Demo:")
    print("-" * 50)
    start, end = get_date_range('7d', 'today')
    print(f"  Last 7 days: {format_date_range(start, end)} ({days_between(start, end)} days)")
