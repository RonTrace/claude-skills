#!/usr/bin/env python3
"""
Stripe API Connection Validator

Tests Stripe API connection and reports status.

Usage:
    python validate_connection.py

Environment Variables Required:
    STRIPE_API_KEY

IMPORTANT: This script will NOT output your API key.
"""

import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import stripe
except ImportError:
    print("ERROR: stripe library is not installed")
    print("Run: pip install stripe")
    sys.exit(1)


def mask_key(key):
    """Mask API key for safe display."""
    if not key:
        return "(not set)"
    if len(key) < 12:
        return "*" * len(key)
    return key[:7] + "*" * (len(key) - 11) + key[-4:]


def validate_connection():
    """Validate Stripe API connection and run basic tests."""
    print("Stripe API Connection Validator")
    print("=" * 50)

    # Check environment variable
    api_key = os.getenv('STRIPE_API_KEY')

    if not api_key:
        print("\nMissing environment variable: STRIPE_API_KEY")
        print("Set this in your .env file or environment.")
        return False

    print("\nEnvironment variables: OK")
    print(f"  Key: {mask_key(api_key)}")

    # Detect mode
    if api_key.startswith('sk_live_'):
        mode = "LIVE"
        print(f"  Mode: {mode} (CAUTION: Production data)")
    elif api_key.startswith('sk_test_'):
        mode = "TEST"
        print(f"  Mode: {mode} (Safe for testing)")
    else:
        mode = "UNKNOWN"
        print(f"  Mode: {mode} (Key format not recognized)")

    # Set API key
    stripe.api_key = api_key

    # Test connection with a simple API call
    print("\nTesting API connection...")
    try:
        # List balance (minimal API call)
        balance = stripe.Balance.retrieve()
        print("  API call: OK")
        print(f"  Account currency: {balance.get('livemode', 'unknown')}")
    except stripe.error.AuthenticationError as e:
        print(f"  ERROR: Authentication failed - {e}")
        return False
    except stripe.error.APIConnectionError as e:
        print(f"  ERROR: Cannot connect to Stripe - {e}")
        return False
    except stripe.error.StripeError as e:
        print(f"  ERROR: {e}")
        return False

    # Test listing customers (common operation)
    print("\nTesting customer list...")
    try:
        customers = stripe.Customer.list(limit=3)
        customer_count = len(customers.data)
        print(f"  Retrieved {customer_count} customers (limited to 3)")

        if customers.data:
            # Show masked email of first customer
            first_email = customers.data[0].get('email', '(no email)')
            if first_email and '@' in first_email:
                local, domain = first_email.split('@')
                masked = local[:2] + '***@' + domain
                print(f"  Sample customer email: {masked}")
    except stripe.error.StripeError as e:
        print(f"  ERROR: {e}")

    # Test listing subscriptions
    print("\nTesting subscription list...")
    try:
        subscriptions = stripe.Subscription.list(limit=3)
        sub_count = len(subscriptions.data)
        print(f"  Retrieved {sub_count} subscriptions (limited to 3)")
    except stripe.error.StripeError as e:
        print(f"  ERROR: {e}")

    print("\nValidation: PASSED")

    # Security reminder
    print("\n" + "=" * 50)
    print("SECURITY REMINDER:")
    print("  - NEVER log or output the full API key")
    print("  - NEVER commit .env files to git")
    print("  - Use test mode (sk_test_) for development")
    print("=" * 50)

    return True


if __name__ == "__main__":
    success = validate_connection()
    sys.exit(0 if success else 1)
