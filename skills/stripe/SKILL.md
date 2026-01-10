---
name: stripe
description: Access Stripe API for payment data. Use when: (1) looking up customer billing info, (2) checking subscription status, (3) viewing charge history, (4) linking payment data to Trace users via email. NEVER log or output the API key. ALWAYS use pagination for list operations.
---

# Stripe API Integration

## Quick Reference

**Setup:**
```python
import stripe
from env_utils import load_env, get_required_env

load_env()
stripe.api_key = get_required_env('STRIPE_API_KEY')
```

**Key Facts:**
- Amounts are in **cents** - divide by 100 for dollars
- Timestamps are **Unix epoch seconds** - use `datetime.fromtimestamp()`
- Link to Trace users via **email**
- Keys starting with `sk_test_` are test mode; `sk_live_` are live

## Pagination

```python
# Gets ALL charges, not just first 100
for charge in stripe.Charge.list(limit=100).auto_paging_iter():
    process(charge)
```

## Common Operations

```python
# Find customer by email
customers = stripe.Customer.list(email=email)
customer = customers.data[0] if customers.data else None

# Get customer subscriptions
subs = stripe.Subscription.list(customer=customer_id, status='active')

# List recent charges
charges = stripe.Charge.list(limit=10)
```

## Linking Stripe to Trace Users

```python
def get_trace_user_subscription(mysql_conn, email):
    # Find in Stripe
    customers = stripe.Customer.list(email=email)
    if not customers.data:
        return None

    customer = customers.data[0]
    subs = stripe.Subscription.list(customer=customer.id, status='active')

    # Find in Trace
    cursor = mysql_conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
    trace_user = cursor.fetchone()

    return {
        'trace_user_id': trace_user['user_id'] if trace_user else None,
        'stripe_customer_id': customer.id,
        'active_subscriptions': len(subs.data)
    }
```

## Rate Limits

Add delays for bulk operations:
```python
import time
for item in items:
    process(item)
    time.sleep(0.1)  # 10 requests per second max
```
