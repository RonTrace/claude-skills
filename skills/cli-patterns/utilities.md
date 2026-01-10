# CLI Utilities

Common utilities for CLI analysis tools.

## Date Parsing

Support flexible date input formats (7d, 2w, 1m, YYYY-MM-DD):

```python
from datetime import datetime, timedelta


def parse_relative_date(date_str):
    """
    Parse relative or absolute date string.

    Args:
        date_str: One of:
            - 'today' - Start of today
            - 'yesterday' - Start of yesterday
            - '7d' - 7 days ago
            - '2w' - 2 weeks ago
            - '1m' - ~1 month ago (30 days)
            - 'YYYY-MM-DD' - Specific date

    Returns:
        datetime object
    """
    date_str = date_str.lower().strip()

    if date_str == 'today':
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_str == 'yesterday':
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    elif date_str.endswith('d'):
        days = int(date_str[:-1])
        return datetime.now() - timedelta(days=days)
    elif date_str.endswith('w'):
        weeks = int(date_str[:-1])
        return datetime.now() - timedelta(weeks=weeks)
    elif date_str.endswith('m'):
        months = int(date_str[:-1])
        return datetime.now() - timedelta(days=months * 30)  # Approximate
    else:
        return datetime.strptime(date_str, '%Y-%m-%d')


def get_date_range(start_str, end_str=None):
    """
    Get start and end dates from strings.

    Args:
        start_str: Start date string
        end_str: End date string (defaults to now)

    Returns:
        Tuple of (start_date, end_date)
    """
    start = parse_relative_date(start_str)
    end = parse_relative_date(end_str) if end_str else datetime.now()
    return start, end
```

### Usage
```python
start_date = parse_relative_date('7d')    # 7 days ago
start_date = parse_relative_date('2w')    # 2 weeks ago
start_date = parse_relative_date('1m')    # ~30 days ago
start_date = parse_relative_date('2025-01-15')  # Specific date

start, end = get_date_range('7d', 'today')
```

## User Lookup

Support both user ID and email:

```python
def resolve_user(connection, identifier):
    """
    Look up user by ID or email.

    Args:
        connection: Database connection
        identifier: User ID (int/str) or email (contains @)

    Returns:
        Dict with user info or None
    """
    cursor = connection.cursor(dictionary=True)

    if '@' in str(identifier):
        cursor.execute("""
            SELECT user_id, email,
                   COALESCE(CONCAT(first_name, ' ', last_name), name) as name
            FROM users WHERE email = %s
        """, (identifier,))
    else:
        cursor.execute("""
            SELECT user_id, email,
                   COALESCE(CONCAT(first_name, ' ', last_name), name) as name
            FROM users WHERE user_id = %s
        """, (int(identifier),))

    result = cursor.fetchone()
    cursor.close()
    return result
```

## Output Formatting

### Console Table
```python
def print_table(headers, rows, min_width=10):
    """Print a formatted ASCII table."""
    # Calculate column widths
    widths = [max(min_width, len(str(h))) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    # Print header
    header_line = ' | '.join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
    print(header_line)
    print('-' * len(header_line))

    # Print rows
    for row in rows:
        print(' | '.join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)))
```

### Number Formatting
```python
def format_number(n):
    """Format number with commas: 1234567 -> 1,234,567"""
    return f"{n:,}"

def format_percent(n, total):
    """Format as percentage: format_percent(25, 100) -> '25.0%'"""
    if total == 0:
        return "N/A"
    return f"{n / total * 100:.1f}%"
```

### Duration Formatting
```python
def format_duration(seconds):
    """Format seconds as human-readable duration."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds / 60:.1f}m"
    else:
        return f"{seconds / 3600:.1f}h"
```

## Argument Parsing

### Standard Arguments
```python
import argparse


def create_parser(description):
    """Create argument parser with common options."""
    parser = argparse.ArgumentParser(description=description)

    # User selection
    parser.add_argument('--user', '-u',
        help='User ID or email')

    # Date range
    parser.add_argument('--start-date', '-s', default='7d',
        help='Start date (7d, 2w, 1m, or YYYY-MM-DD)')
    parser.add_argument('--end-date', '-e',
        help='End date (default: now)')

    # Output options
    parser.add_argument('--output', '-o',
        choices=['console', 'csv', 'json'],
        default='console',
        help='Output format')
    parser.add_argument('--output-file', '-f',
        help='Output file path')

    return parser
```

### Usage
```python
parser = create_parser('Analyze user activity')
parser.add_argument('--team', help='Filter by team ID')  # Add custom args
args = parser.parse_args()
```

## Error Handling

```python
import sys


def error_exit(message, code=1):
    """Print error and exit."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(code)


def handle_db_error(e):
    """Handle database errors gracefully."""
    if "Connection" in str(e):
        error_exit("Database connection failed. Check your .env file.")
    elif "Access denied" in str(e):
        error_exit("Database access denied. Check credentials.")
    else:
        error_exit(f"Database error: {e}")
```

## CSV Export

```python
import csv


def export_to_csv(filename, headers, rows):
    """Export data to CSV file."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Exported to {filename}")


def export_dicts_to_csv(filename, data):
    """Export list of dicts to CSV."""
    if not data:
        print("No data to export")
        return

    headers = data[0].keys()
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    print(f"Exported {len(data)} rows to {filename}")
```

## JSON Output

```python
import json
from datetime import datetime


class DateEncoder(json.JSONEncoder):
    """JSON encoder that handles datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def export_to_json(filename, data):
    """Export data to JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, cls=DateEncoder)
    print(f"Exported to {filename}")
```
