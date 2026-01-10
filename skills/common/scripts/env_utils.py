#!/usr/bin/env python3
"""
Environment Variable Utilities

Safe environment variable handling for Trace skills.

Usage:
    from env_utils import load_env, get_required_env, get_optional_env

    load_env()  # Load from .env file
    api_key = get_required_env('STRIPE_API_KEY')  # Raises if missing
    debug = get_optional_env('DEBUG', 'false')    # Returns default if missing
"""

import os
import sys
from typing import Optional


def load_env(env_file: str = '.env') -> bool:
    """
    Load environment variables from a .env file.

    Args:
        env_file: Path to .env file (default '.env')

    Returns:
        True if file was loaded, False if file not found
    """
    try:
        from dotenv import load_dotenv
        if os.path.exists(env_file):
            load_dotenv(env_file)
            return True
        else:
            # Try parent directories
            current = os.getcwd()
            while current != '/':
                potential = os.path.join(current, env_file)
                if os.path.exists(potential):
                    load_dotenv(potential)
                    return True
                current = os.path.dirname(current)
            return False
    except ImportError:
        # dotenv not installed, rely on system env vars
        return False


def get_required_env(name: str, description: Optional[str] = None) -> str:
    """
    Get a required environment variable.

    Args:
        name: Environment variable name
        description: Optional description for error message

    Returns:
        The environment variable value

    Raises:
        SystemExit: If the variable is not set
    """
    value = os.getenv(name)
    if value is None:
        msg = f"Error: Required environment variable '{name}' is not set."
        if description:
            msg += f" ({description})"
        msg += "\nCheck your .env file or set the variable in your environment."
        print(msg, file=sys.stderr)
        sys.exit(1)
    return value


def get_optional_env(name: str, default: str = '') -> str:
    """
    Get an optional environment variable with a default.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        The environment variable value or default
    """
    return os.getenv(name, default)


def get_bool_env(name: str, default: bool = False) -> bool:
    """
    Get a boolean environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set

    Returns:
        True if value is 'true', '1', 'yes' (case-insensitive), False otherwise
    """
    value = os.getenv(name, '').lower()
    if not value:
        return default
    return value in ('true', '1', 'yes', 'on')


def get_int_env(name: str, default: int = 0) -> int:
    """
    Get an integer environment variable.

    Args:
        name: Environment variable name
        default: Default value if not set or invalid

    Returns:
        The integer value or default
    """
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def check_env_vars(required: list, optional: list = None) -> dict:
    """
    Check multiple environment variables at once.

    Args:
        required: List of required variable names
        optional: List of optional variable names

    Returns:
        Dict with all variable values

    Raises:
        SystemExit: If any required variable is missing
    """
    result = {}
    missing = []

    for name in required:
        value = os.getenv(name)
        if value is None:
            missing.append(name)
        else:
            result[name] = value

    if missing:
        print(f"Error: Missing required environment variables:", file=sys.stderr)
        for name in missing:
            print(f"  - {name}", file=sys.stderr)
        print("\nCheck your .env file or set these variables in your environment.", file=sys.stderr)
        sys.exit(1)

    if optional:
        for name in optional:
            result[name] = os.getenv(name, '')

    return result


def mask_secret(value: str, visible_chars: int = 4) -> str:
    """
    Mask a secret value for safe logging.

    Args:
        value: The secret value
        visible_chars: Number of characters to show at the end

    Returns:
        Masked string like "****1234"
    """
    if len(value) <= visible_chars:
        return '*' * len(value)
    return '*' * (len(value) - visible_chars) + value[-visible_chars:]


if __name__ == "__main__":
    print("Environment Utilities Demo")
    print("=" * 40)

    # Try to load .env
    loaded = load_env()
    print(f"\n.env file loaded: {loaded}")

    # Show current env status
    print("\nDatabase Connection Status:")

    mysql_vars = ['MYSQL_HOST', 'MYSQL_DATABASE', 'MYSQL_USER', 'MYSQL_PASSWORD']
    for var in mysql_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var:
                print(f"  {var}: {mask_secret(value)}")
            else:
                print(f"  {var}: {value}")
        else:
            print(f"  {var}: NOT SET")

    print("\nRedshift Connection Status:")
    redshift_vars = ['REDSHIFT_HOST', 'REDSHIFT_DATABASE', 'REDSHIFT_USER', 'REDSHIFT_PASSWORD']
    for var in redshift_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var:
                print(f"  {var}: {mask_secret(value)}")
            else:
                print(f"  {var}: {value}")
        else:
            print(f"  {var}: NOT SET")

    print("\nStripe Status:")
    stripe_key = os.getenv('STRIPE_API_KEY')
    if stripe_key:
        mode = "LIVE" if stripe_key.startswith('sk_live_') else "TEST"
        print(f"  STRIPE_API_KEY: {mask_secret(stripe_key)} ({mode} mode)")
    else:
        print("  STRIPE_API_KEY: NOT SET")
