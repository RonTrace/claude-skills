# Schema Exploration

Use this for:
- Tables NOT documented in Reference Files
- Discovering column values or data distributions
- Validating assumptions about undocumented columns

**Before exploring:** Check if the table has a doc in `tables/`. If it does, read the gotchas there first.

---

## Discovering Schema

### List All Schemas
```python
cursor.execute("""
    SELECT schema_name
    FROM information_schema.schemata
    ORDER BY schema_name
""")
for row in cursor.fetchall():
    print(row[0])
```

### List Tables in Schema
```python
cursor.execute("""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'tracedb'
    ORDER BY table_name
""")
```

### Describe Table Columns
```python
cursor.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns
    WHERE table_schema = 'tracedb'
    AND table_name = 'tracked_actions'
    ORDER BY ordinal_position
""")
for col in cursor.fetchall():
    print(f"{col[0]}: {col[1]} (nullable: {col[2]})")
```

### Find Tables by Name Pattern
```python
cursor.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_name LIKE '%division%'
""")
```

## Sampling Data

### Quick Sample
```python
cursor.execute("SELECT * FROM tracedb.tracked_actions LIMIT 10")
for row in cursor.fetchall():
    print(row)
```

### With Column Names
```python
from psycopg2.extras import RealDictCursor

cursor = connection.cursor(cursor_factory=RealDictCursor)
cursor.execute("SELECT * FROM tracedb.tracked_actions LIMIT 5")
for row in cursor.fetchall():
    print(dict(row))
```

### Random Sample
```python
# Redshift: Use RANDOM() instead of RAND()
cursor.execute("""
    SELECT * FROM tracedb.tracked_actions
    WHERE RANDOM() < 0.001  -- 0.1% sample
    LIMIT 100
""")
```

## Validating Data

### Check Table Size
```python
cursor.execute("""
    SELECT COUNT(*) FROM tracedb.tracked_actions
    WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '1 day'
""")
print(f"Records in last day: {cursor.fetchone()[0]:,}")
```

### Check Date Range
```python
cursor.execute("""
    SELECT
        MIN(creation_time) as earliest,
        MAX(creation_time) as latest
    FROM tracedb.tracked_actions
""")
```

### Check for NULLs
```python
cursor.execute("""
    SELECT
        COUNT(*) as total,
        COUNT(acting_user_id) as with_user,
        COUNT(*) - COUNT(acting_user_id) as null_users
    FROM tracedb.tracked_actions
    WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '7 days'
""")
```

### Check Distinct Values
```python
cursor.execute("""
    SELECT action_category, COUNT(*) as cnt
    FROM tracedb.tracked_actions
    WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '7 days'
    GROUP BY action_category
    ORDER BY cnt DESC
    LIMIT 20
""")
```

## Testing Queries

### Validate Totals
```python
# Total should match sum of parts
cursor.execute("""
    SELECT COUNT(*) FROM tracedb.tracked_actions
    WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '7 days'
""")
total = cursor.fetchone()[0]

cursor.execute("""
    SELECT action_category, COUNT(*) as cnt
    FROM tracedb.tracked_actions
    WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '7 days'
    GROUP BY action_category
""")
parts_sum = sum(row[1] for row in cursor.fetchall())

assert total == parts_sum, f"Mismatch: {total} vs {parts_sum}"
```

### Test Date Functions
```python
# Verify date truncation works as expected
cursor.execute("""
    SELECT
        creation_time,
        DATE_TRUNC('day', creation_time) as day,
        DATE_TRUNC('week', creation_time) as week,
        DATE_TRUNC('month', creation_time) as month
    FROM tracedb.tracked_actions
    LIMIT 5
""")
```

### Check Query Performance
```python
import time

start = time.time()
cursor.execute("""
    SELECT COUNT(DISTINCT acting_user_id)
    FROM tracedb.tracked_actions
    WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '30 days'
""")
elapsed = time.time() - start
print(f"Query took {elapsed:.2f} seconds")
```

## Redshift-Specific Gotchas

### No Dictionary Cursor by Default
```python
# Manual dict conversion
cursor.execute("SELECT user_id, email FROM users LIMIT 5")
columns = [desc[0] for desc in cursor.description]
for row in cursor.fetchall():
    record = dict(zip(columns, row))
    print(record)

# Or use RealDictCursor
from psycopg2.extras import RealDictCursor
cursor = connection.cursor(cursor_factory=RealDictCursor)
```

### String Concatenation
```python
# WRONG - MySQL syntax
cursor.execute("SELECT CONCAT(first_name, ' ', last_name) FROM users")

# RIGHT - Redshift syntax
cursor.execute("SELECT first_name || ' ' || last_name FROM users")
```

### Date Functions
```python
# WRONG - MySQL syntax
cursor.execute("SELECT DATE(creation_time) FROM tracked_actions")

# RIGHT - Redshift syntax
cursor.execute("SELECT DATE_TRUNC('day', creation_time) FROM tracked_actions")
```

### Schema Prefix
```python
# Always use schema prefix or set search_path
cursor.execute("SELECT * FROM tracedb.tracked_actions LIMIT 5")
# Or after SET search_path TO tracedb:
cursor.execute("SELECT * FROM tracked_actions LIMIT 5")
```

## When to Ask User for Clarification

- **Schema uncertainty**: "Should I use tracedb.divisions or dbt_prod.divisions?"
- **Pre-aggregated vs raw**: "Should I compute from tracked_actions or use the pre-aggregated table?"
- **Performance concerns**: "This query on 100M rows will take ~5 minutes. Want me to proceed?"
- **Data freshness**: "Redshift data may be up to 24 hours old. Is that acceptable?"
