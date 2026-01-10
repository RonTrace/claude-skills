---
name: cli-patterns
description: Reusable patterns for Python CLI tools. Use when: (1) building a command-line analysis tool, (2) needing spinners/progress feedback, (3) parsing date arguments (7d, 2w, 1m), (4) formatting console/CSV/JSON output. Provides Spinner class, date parsing, table formatting, and export utilities.
---

# CLI Tool Patterns

## Quick Reference

**Date Parsing:** Supports `7d`, `2w`, `1m`, `today`, `yesterday`, `YYYY-MM-DD`

**Spinner Usage:**
```python
from spinner import Spinner
spinner = Spinner("Loading data")
spinner.start()
# ... do work ...
spinner.stop()
```

**Standard Arguments:**
- `--user` / `-u` - User ID or email
- `--start-date` / `-s` - Start date (default: 7d)
- `--output` / `-o` - Format: console, csv, json

**Dependencies:** `mysql-connector-python`, `psycopg2-binary`, `python-dotenv`

Reusable patterns for building command-line analysis tools at Trace.

## Standard Tool Structure

```python
#!/usr/bin/env python3
"""
Tool Name - Brief description

Usage:
    python tool_name.py [options]

Examples:
    python tool_name.py --user 12345
    python tool_name.py --email user@example.com --start-date 7d
"""

import argparse
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import patterns from this skill
# from spinner import Spinner  (see spinner.md)
# from utils import parse_relative_date  (see utilities.md)


def get_connection():
    """Database connection - see mysql or redshift skill"""
    pass


def main():
    parser = argparse.ArgumentParser(description='Tool description')
    parser.add_argument('--user', help='User ID or email')
    parser.add_argument('--start-date', default='7d', help='Start date (7d, 2w, 1m, or YYYY-MM-DD)')
    args = parser.parse_args()

    # Initialize
    connection = get_connection()

    try:
        # Show progress
        spinner = Spinner("Loading data")
        spinner.start()

        # Do work
        results = fetch_data(connection, args.user)

        spinner.stop()

        # Output results
        print_results(results)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
```

---

## 📚 Reference Files

| File | Contains | Read When... |
|------|----------|--------------|
| [spinner.md](spinner.md) | Spinner class implementation, TTY detection, animation patterns, usage examples | Adding progress feedback to CLI tools |
| [utilities.md](utilities.md) | Date parsing (7d, 2w, 1m), table formatting, CSV/JSON export, error handling patterns | Parsing arguments, formatting output, or handling errors |

## Reference Examples

These tools demonstrate best practices:

- **roster_cohorts_analysis.py** - Data fetcher pattern, HTML generation
- **division_cohorts_analysis.py** - Cohort analysis with multiple data sources
- **upcoming_games_all.py** - Clean CLI structure with dictionary cursor

## Best Practices

1. **Always use spinners** for operations that take more than a second
2. **Support flexible date inputs** (7d, 2w, 1m, YYYY-MM-DD)
3. **Handle piped output** - spinners auto-detect TTY
4. **Use dictionary cursors** for readable code
5. **Close connections in finally blocks**
6. **Print errors to stderr**, results to stdout
7. **Support both user ID and email lookups**
8. **Document usage in docstring**

