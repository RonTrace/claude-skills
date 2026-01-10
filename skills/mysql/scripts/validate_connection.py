#!/usr/bin/env python3
"""
MySQL Connection Validator

Tests MySQL database connection and reports status.

Usage:
    python validate_connection.py

Environment Variables Required:
    MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from mysql.connector import connect, Error
except ImportError:
    print("ERROR: mysql-connector-python is not installed")
    print("Run: pip install mysql-connector-python")
    sys.exit(1)


def validate_connection():
    """Validate MySQL connection and run basic tests."""
    print("MySQL Connection Validator")
    print("=" * 50)

    # Check environment variables
    required_vars = ['MYSQL_HOST', 'MYSQL_DATABASE', 'MYSQL_USER', 'MYSQL_PASSWORD']
    missing = [v for v in required_vars if not os.getenv(v)]

    if missing:
        print("\nMissing environment variables:")
        for v in missing:
            print(f"  - {v}")
        print("\nSet these in your .env file or environment.")
        return False

    print("\nEnvironment variables: OK")

    # Test connection
    print("\nConnecting to MySQL...")
    try:
        connection = connect(
            host=os.getenv('MYSQL_HOST'),
            port=3306,
            database=os.getenv('MYSQL_DATABASE'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD')
        )
        print(f"  Host: {os.getenv('MYSQL_HOST')}")
        print(f"  Database: {os.getenv('MYSQL_DATABASE')}")
        print("  Status: CONNECTED")
    except Error as e:
        print(f"  ERROR: {e}")
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
    except Error as e:
        print(f"  ERROR: {e}")
        connection.close()
        return False

    # Test table access
    print("\nChecking table access...")
    try:
        cursor = connection.cursor()

        # Check users table
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"  users table: {user_count:,} rows")

        # Check teams table
        cursor.execute("SELECT COUNT(*) FROM teams")
        team_count = cursor.fetchone()[0]
        print(f"  teams table: {team_count:,} rows")

        # Check tracked_actions table (with date limit)
        cursor.execute("""
            SELECT COUNT(*) FROM tracked_actions
            WHERE creation_time >= DATE_SUB(NOW(), INTERVAL 1 DAY)
        """)
        action_count = cursor.fetchone()[0]
        print(f"  tracked_actions (last 24h): {action_count:,} rows")

        cursor.close()
    except Error as e:
        print(f"  ERROR: {e}")
        print("  Some tables may not be accessible.")

    connection.close()
    print("\nConnection closed.")
    print("\nValidation: PASSED")
    return True


if __name__ == "__main__":
    success = validate_connection()
    sys.exit(0 if success else 1)
