#!/usr/bin/env python3
"""
Database Connection Utilities

Centralized database connection management for Trace skills.
Handles MySQL and Redshift connections with proper error handling.

Usage:
    from connections import get_mysql_connection, get_redshift_connection

    # MySQL
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users LIMIT 10")
    conn.close()

    # Redshift
    conn = get_redshift_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracedb.users LIMIT 10")
    conn.close()

Environment Variables Required:
    MySQL: MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
    Redshift: REDSHIFT_HOST, REDSHIFT_DATABASE, REDSHIFT_USER, REDSHIFT_PASSWORD, REDSHIFT_SCHEMA
"""

import os
import sys
from typing import Optional

# Try to import database drivers
try:
    from mysql.connector import connect as mysql_connect, Error as MySQLError
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False
    MySQLError = Exception

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    REDSHIFT_AVAILABLE = True
except ImportError:
    REDSHIFT_AVAILABLE = False
    RealDictCursor = None

# Try to load dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required if env vars are set directly


def get_mysql_connection(
    host: Optional[str] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    port: int = 3306
):
    """
    Get a MySQL database connection.

    Args:
        host: Database host (defaults to MYSQL_HOST env var)
        database: Database name (defaults to MYSQL_DATABASE env var)
        user: Username (defaults to MYSQL_USER env var)
        password: Password (defaults to MYSQL_PASSWORD env var)
        port: Port number (default 3306)

    Returns:
        MySQL connection object

    Raises:
        RuntimeError: If mysql-connector-python is not installed
        SystemExit: If connection fails
    """
    if not MYSQL_AVAILABLE:
        raise RuntimeError(
            "mysql-connector-python is not installed. "
            "Run: pip install mysql-connector-python"
        )

    config = {
        'host': host or os.getenv('MYSQL_HOST'),
        'database': database or os.getenv('MYSQL_DATABASE'),
        'user': user or os.getenv('MYSQL_USER'),
        'password': password or os.getenv('MYSQL_PASSWORD'),
        'port': port,
    }

    # Validate required fields
    missing = [k for k, v in config.items() if v is None and k != 'port']
    if missing:
        print(f"Error: Missing MySQL configuration: {', '.join(missing)}", file=sys.stderr)
        print("Set these as environment variables or pass as arguments.", file=sys.stderr)
        sys.exit(1)

    try:
        connection = mysql_connect(**config)
        return connection
    except MySQLError as e:
        print(f"Error connecting to MySQL: {e}", file=sys.stderr)
        if "Access denied" in str(e):
            print("Check your MYSQL_USER and MYSQL_PASSWORD.", file=sys.stderr)
        elif "Unknown database" in str(e):
            print("Check your MYSQL_DATABASE.", file=sys.stderr)
        elif "Can't connect" in str(e):
            print("Check your MYSQL_HOST and ensure the database is accessible.", file=sys.stderr)
        sys.exit(1)


def get_redshift_connection(
    host: Optional[str] = None,
    database: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    port: int = 5439,
    schema: Optional[str] = None,
    autocommit: bool = True
):
    """
    Get a Redshift database connection.

    Args:
        host: Cluster host (defaults to REDSHIFT_HOST env var)
        database: Database name (defaults to REDSHIFT_DATABASE env var)
        user: Username (defaults to REDSHIFT_USER env var)
        password: Password (defaults to REDSHIFT_PASSWORD env var)
        port: Port number (default 5439)
        schema: Default schema to set (defaults to REDSHIFT_SCHEMA env var)
        autocommit: Enable autocommit mode (default True, required for Redshift)

    Returns:
        Redshift/psycopg2 connection object

    Raises:
        RuntimeError: If psycopg2 is not installed
        SystemExit: If connection fails
    """
    if not REDSHIFT_AVAILABLE:
        raise RuntimeError(
            "psycopg2 is not installed. "
            "Run: pip install psycopg2-binary"
        )

    config = {
        'host': host or os.getenv('REDSHIFT_HOST'),
        'database': database or os.getenv('REDSHIFT_DATABASE'),
        'user': user or os.getenv('REDSHIFT_USER'),
        'password': password or os.getenv('REDSHIFT_PASSWORD'),
        'port': port,
    }
    schema = schema or os.getenv('REDSHIFT_SCHEMA', 'tracedb')

    # Validate required fields
    missing = [k for k, v in config.items() if v is None and k != 'port']
    if missing:
        print(f"Error: Missing Redshift configuration: {', '.join(missing)}", file=sys.stderr)
        print("Set these as environment variables or pass as arguments.", file=sys.stderr)
        sys.exit(1)

    try:
        connection = psycopg2.connect(**config)
        connection.autocommit = autocommit

        # Set default schema
        if schema:
            cursor = connection.cursor()
            cursor.execute(f"SET search_path TO {schema}")
            cursor.close()

        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to Redshift: {e}", file=sys.stderr)
        if "authentication failed" in str(e).lower():
            print("Check your REDSHIFT_USER and REDSHIFT_PASSWORD.", file=sys.stderr)
        elif "could not connect" in str(e).lower():
            print("Check your REDSHIFT_HOST and port (should be 5439).", file=sys.stderr)
        sys.exit(1)


def get_redshift_dict_cursor(connection):
    """
    Get a dictionary cursor for Redshift.

    Args:
        connection: Redshift connection object

    Returns:
        Cursor that returns rows as dictionaries
    """
    if not REDSHIFT_AVAILABLE:
        raise RuntimeError("psycopg2 is not installed")
    return connection.cursor(cursor_factory=RealDictCursor)


def test_mysql_connection() -> bool:
    """Test MySQL connection and return True if successful."""
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


def test_redshift_connection() -> bool:
    """Test Redshift connection and return True if successful."""
    try:
        conn = get_redshift_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    print("Testing database connections...")
    print("-" * 40)

    # Test MySQL
    print("\nMySQL:", end=" ")
    if MYSQL_AVAILABLE:
        if test_mysql_connection():
            print("OK")
        else:
            print("FAILED (check credentials)")
    else:
        print("SKIPPED (mysql-connector-python not installed)")

    # Test Redshift
    print("Redshift:", end=" ")
    if REDSHIFT_AVAILABLE:
        if test_redshift_connection():
            print("OK")
        else:
            print("FAILED (check credentials)")
    else:
        print("SKIPPED (psycopg2 not installed)")
