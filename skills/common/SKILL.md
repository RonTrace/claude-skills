---
name: common
description: Shared utilities for all Trace skills. Use when: (1) needing database connections (MySQL/Redshift), (2) loading environment variables, (3) using common helpers across skills. This skill provides the foundation that other skills build upon.
---

# Trace Common Utilities

## Scripts

### `scripts/connections.py`

Database connections with proper error handling:

```python
from connections import get_mysql_connection, get_redshift_connection, get_redshift_dict_cursor

# MySQL (supports dictionary=True cursor)
conn = get_mysql_connection()
cursor = conn.cursor(dictionary=True)

# Redshift (autocommit=True, schema set automatically)
conn = get_redshift_connection()
cursor = get_redshift_dict_cursor(conn)  # For dict-like row access
```

Run `python scripts/connections.py` to test connections.

### `scripts/env_utils.py`

Environment variable handling:

```python
from env_utils import load_env, get_required_env, get_optional_env

load_env()  # Loads .env, searches parent dirs if needed
api_key = get_required_env('STRIPE_API_KEY')  # Exits if missing
debug = get_optional_env('DEBUG', 'false')
```

## Environment Variables

| Variable | Used By |
|----------|---------|
| MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD | MySQL |
| REDSHIFT_HOST, REDSHIFT_DATABASE, REDSHIFT_USER, REDSHIFT_PASSWORD, REDSHIFT_SCHEMA | Redshift |
| STRIPE_API_KEY | Stripe |
