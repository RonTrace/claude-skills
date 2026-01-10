#!/usr/bin/env python3
"""
Redshift Connection Validator

Tests Redshift database connection and reports status.

Usage:
    python validate_connection.py

Environment Variables Required:
    REDSHIFT_HOST, REDSHIFT_DATABASE, REDSHIFT_USER, REDSHIFT_PASSWORD
    Optional: REDSHIFT_SCHEMA (defaults to 'tracedb')
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import psycopg2
except ImportError:
    print("ERROR: psycopg2 is not installed")
    print("Run: pip install psycopg2-binary")
    sys.exit(1)


def validate_connection():
    """Validate Redshift connection and run basic tests."""
    print("Redshift Connection Validator")
    print("=" * 50)

    # Check environment variables
    required_vars = ['REDSHIFT_HOST', 'REDSHIFT_DATABASE', 'REDSHIFT_USER', 'REDSHIFT_PASSWORD']
    missing = [v for v in required_vars if not os.getenv(v)]

    if missing:
        print("\nMissing environment variables:")
        for v in missing:
            print(f"  - {v}")
        print("\nSet these in your .env file or environment.")
        return False

    print("\nEnvironment variables: OK")

    # Test connection
    print("\nConnecting to Redshift...")
    schema = os.getenv('REDSHIFT_SCHEMA', 'tracedb')

    try:
        connection = psycopg2.connect(
            host=os.getenv('REDSHIFT_HOST'),
            port=5439,
            database=os.getenv('REDSHIFT_DATABASE'),
            user=os.getenv('REDSHIFT_USER'),
            password=os.getenv('REDSHIFT_PASSWORD')
        )
        connection.autocommit = True
        print(f"  Host: {os.getenv('REDSHIFT_HOST')}")
        print(f"  Database: {os.getenv('REDSHIFT_DATABASE')}")
        print(f"  Port: 5439")
        print("  Status: CONNECTED")
    except psycopg2.Error as e:
        print(f"  ERROR: {e}")
        return False

    # Set search path
    print(f"\nSetting search_path to '{schema}'...")
    try:
        cursor = connection.cursor()
        cursor.execute(f"SET search_path TO {schema}")
        print(f"  search_path: OK")
        cursor.close()
    except psycopg2.Error as e:
        print(f"  ERROR: {e}")
        connection.close()
        return False

    # Test basic query
    print("\nRunning test query...")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        if result[0] == 1:
            print("  SELECT 1: OK")
        cursor.close()
    except psycopg2.Error as e:
        print(f"  ERROR: {e}")
        connection.close()
        return False

    # Test SQL syntax (Redshift uses PostgreSQL syntax)
    print("\nTesting PostgreSQL syntax...")
    try:
        cursor = connection.cursor()

        # String concat with ||
        cursor.execute("SELECT 'hello' || ' ' || 'world'")
        result = cursor.fetchone()[0]
        print(f"  String concat (||): '{result}' - OK")

        # DATE_TRUNC
        cursor.execute("SELECT DATE_TRUNC('day', CURRENT_TIMESTAMP)")
        result = cursor.fetchone()[0]
        print(f"  DATE_TRUNC: {result} - OK")

        # INTERVAL syntax
        cursor.execute("SELECT CURRENT_TIMESTAMP - INTERVAL '7 days'")
        result = cursor.fetchone()[0]
        print(f"  INTERVAL syntax: OK")

        cursor.close()
    except psycopg2.Error as e:
        print(f"  ERROR: {e}")

    # Test table access
    print("\nChecking table access...")
    try:
        cursor = connection.cursor()

        # Check tracked_actions in tracedb
        cursor.execute(f"""
            SELECT COUNT(*) FROM {schema}.tracked_actions
            WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '1 day'
        """)
        action_count = cursor.fetchone()[0]
        print(f"  {schema}.tracked_actions (last 24h): {action_count:,} rows")

        # Check dbt_prod schema
        cursor.execute("""
            SELECT COUNT(*) FROM dbt_prod.flex_watch_divisions_over_games
        """)
        div_count = cursor.fetchone()[0]
        print(f"  dbt_prod.flex_watch_divisions_over_games: {div_count:,} rows")

        cursor.close()
    except psycopg2.Error as e:
        print(f"  ERROR: {e}")
        print("  Some tables may not be accessible.")

    connection.close()
    print("\nConnection closed.")
    print("\nValidation: PASSED")
    return True


if __name__ == "__main__":
    success = validate_connection()
    sys.exit(0 if success else 1)
