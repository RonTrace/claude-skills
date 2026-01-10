# Sample Data Inspection

Techniques for spot-checking data to verify correctness.

## Quick Sample

Start with a simple sample to understand the data:

```python
cursor.execute("SELECT * FROM table_name LIMIT 10")
for row in cursor.fetchall():
    print(row)
```

**Use dictionary cursor for readability:**
```python
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT * FROM users LIMIT 5")
for row in cursor.fetchall():
    print(f"User {row['user_id']}: {row['email']}")
```

## Random Sampling

Get a representative sample across the dataset:

```python
# MySQL random sample
cursor.execute("SELECT * FROM users ORDER BY RAND() LIMIT 10")

# Faster for large tables (approximate)
cursor.execute("""
    SELECT * FROM tracked_actions
    WHERE RAND() < 0.001  -- ~0.1% sample
    LIMIT 100
""")
```

## Conditional Sampling

Sample data matching specific conditions:

```python
# See what data looks like for a specific user
cursor.execute("""
    SELECT * FROM tracked_actions
    WHERE acting_user_id = %s
    ORDER BY creation_time DESC
    LIMIT 20
""", (sample_user_id,))

# Sample from each category
cursor.execute("""
    SELECT action_category, action_name, creation_time
    FROM tracked_actions
    WHERE creation_time >= %s
    GROUP BY action_category
    ORDER BY action_category
""", (start_date,))
```

## Known Record Verification

Verify records you know should exist:

```python
# If you know what a specific user should look like
known_user_id = 12345
expected_email = "known.user@example.com"

cursor.execute("SELECT email FROM users WHERE user_id = %s", (known_user_id,))
result = cursor.fetchone()

if result and result[0] == expected_email:
    print("Spot check PASSED")
else:
    print(f"Spot check FAILED: Expected {expected_email}, got {result}")
```

**Build a verification set:**
```python
KNOWN_RECORDS = [
    {"user_id": 12345, "email": "user1@example.com"},
    {"user_id": 67890, "email": "user2@example.com"},
    # Add more known records
]

def verify_known_records(cursor):
    passed = 0
    failed = 0
    for record in KNOWN_RECORDS:
        cursor.execute("SELECT email FROM users WHERE user_id = %s", (record["user_id"],))
        result = cursor.fetchone()
        if result and result[0] == record["email"]:
            passed += 1
        else:
            failed += 1
            print(f"FAILED: user_id {record['user_id']}")

    print(f"Spot check: {passed}/{len(KNOWN_RECORDS)} passed")
    return failed == 0
```

## Edge Case Inspection

Check boundary values:

```python
# Find MIN and MAX values
cursor.execute("""
    SELECT
        MIN(creation_time) as earliest,
        MAX(creation_time) as latest,
        MIN(user_id) as min_id,
        MAX(user_id) as max_id
    FROM tracked_actions
    WHERE creation_time >= %s
""", (start_date,))

result = cursor.fetchone()
print(f"Date range: {result[0]} to {result[1]}")
print(f"User ID range: {result[2]} to {result[3]}")

# Inspect edge records
cursor.execute("""
    SELECT * FROM tracked_actions
    WHERE creation_time = (SELECT MIN(creation_time) FROM tracked_actions WHERE creation_time >= %s)
""", (start_date,))
print("Earliest record:", cursor.fetchone())
```

## Manual Calculation Comparison

Verify aggregates by calculating manually:

```python
# Get aggregated result
cursor.execute("""
    SELECT team_id, COUNT(*) as player_count
    FROM team_players
    WHERE team_id = %s AND leave_time IS NULL
    GROUP BY team_id
""", (team_id,))
aggregated = cursor.fetchone()

# Get raw records
cursor.execute("""
    SELECT user_id, is_player, is_coach
    FROM team_players
    WHERE team_id = %s AND leave_time IS NULL
""", (team_id,))
raw = cursor.fetchall()

# Compare
print(f"Aggregated count: {aggregated[1]}")
print(f"Manual count: {len(raw)}")
print(f"Sample records:")
for row in raw[:5]:
    print(f"  User {row[0]}: player={row[1]}, coach={row[2]}")
```

## Visual Inspection Workflow

Systematic approach to inspecting new data:

```python
def inspect_table(cursor, table_name, sample_size=10):
    """Visual inspection of a table's data."""

    print(f"\n=== Inspecting {table_name} ===\n")

    # 1. Row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    print(f"Total rows: {cursor.fetchone()[0]:,}")

    # 2. Column info
    cursor.execute(f"DESCRIBE {table_name}")
    print("\nColumns:")
    for col in cursor.fetchall():
        print(f"  {col[0]}: {col[1]}")

    # 3. Sample data
    cursor.execute(f"SELECT * FROM {table_name} LIMIT {sample_size}")
    print(f"\nSample ({sample_size} rows):")
    for row in cursor.fetchall():
        print(f"  {row}")

    # 4. Date range (if applicable)
    cursor.execute(f"DESCRIBE {table_name}")
    columns = [col[0] for col in cursor.fetchall()]
    date_cols = [c for c in columns if 'time' in c.lower() or 'date' in c.lower()]

    for col in date_cols:
        cursor.execute(f"SELECT MIN({col}), MAX({col}) FROM {table_name}")
        min_date, max_date = cursor.fetchone()
        print(f"\n{col} range: {min_date} to {max_date}")
```

## Comparison Sampling

Compare samples from different sources:

```python
def compare_samples(mysql_cursor, redshift_cursor, query, params, sample_size=5):
    """Compare samples from MySQL and Redshift."""

    mysql_cursor.execute(query + f" LIMIT {sample_size}", params)
    mysql_rows = mysql_cursor.fetchall()

    redshift_cursor.execute(query + f" LIMIT {sample_size}", params)
    redshift_rows = redshift_cursor.fetchall()

    print("MySQL sample:")
    for row in mysql_rows:
        print(f"  {row}")

    print("\nRedshift sample:")
    for row in redshift_rows:
        print(f"  {row}")

    return mysql_rows, redshift_rows
```

## Inspection Checklist

When inspecting unfamiliar data:

1. **Count total rows** - Understand scale
2. **Check date range** - Verify time coverage
3. **Sample 10 random rows** - Eyeball the data
4. **Check NULLs in key columns** - Identify gaps
5. **List distinct values** - Understand cardinality
6. **Verify 2-3 known records** - Confirm expected values
7. **Check edge cases** - MIN/MAX values
8. **Look for anomalies** - Future dates, negative IDs
