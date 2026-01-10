# Query Result Validation Patterns

Techniques to verify your query results are correct.

## Totals Reconciliation

The sum of parts should always equal the whole:

```python
# Get total
cursor.execute("SELECT COUNT(*) FROM tracked_actions WHERE creation_time >= %s", (start_date,))
total = cursor.fetchone()[0]

# Get parts
cursor.execute("""
    SELECT action_category, COUNT(*) as count
    FROM tracked_actions
    WHERE creation_time >= %s
    GROUP BY action_category
""", (start_date,))
parts_sum = sum(row[1] for row in cursor.fetchall())

# Validate
if total != parts_sum:
    print(f"WARNING: Total ({total}) != Sum of parts ({parts_sum})")
else:
    print(f"Validated: {total} records")
```

**When totals don't match:**
- Check for NULL values in the GROUP BY column
- Look for filters applied inconsistently
- Verify date ranges are identical

## NULL Checks

Always check NULL rates in key columns:

```python
# How many NULLs in a column?
cursor.execute("SELECT COUNT(*) FROM users WHERE first_name IS NULL")
null_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM users")
total = cursor.fetchone()[0]

null_rate = null_count / total * 100
print(f"NULLs: {null_count}/{total} ({null_rate:.1f}%)")

# Flag unexpected NULL rates
if null_rate > 10:
    print("WARNING: High NULL rate - investigate before proceeding")
```

## Distinct Value Check

Verify columns contain expected values:

```python
# What values exist?
cursor.execute("SELECT DISTINCT status FROM subscriptions")
print("Distinct statuses:", [row[0] for row in cursor.fetchall()])

# With counts
cursor.execute("""
    SELECT status, COUNT(*) as count
    FROM subscriptions
    GROUP BY status
    ORDER BY count DESC
""")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")
```

**Watch for:**
- Unexpected values (typos, legacy data)
- Missing expected values
- Single value dominating (might not be useful for analysis)

## Date Range Validation

Verify data covers expected time period:

```python
cursor.execute("""
    SELECT
        MIN(creation_time) as earliest,
        MAX(creation_time) as latest,
        COUNT(*) as total
    FROM tracked_actions
    WHERE creation_time >= %s AND creation_time < %s
""", (start_date, end_date))

earliest, latest, total = cursor.fetchone()
print(f"Data range: {earliest} to {latest}")
print(f"Total records: {total}")

# Validate
if earliest > start_date:
    print(f"WARNING: Data starts later than expected ({earliest} vs {start_date})")
if latest < end_date:
    print(f"WARNING: Data ends earlier than expected ({latest} vs {end_date})")
```

## Duplicate Detection

Catch unintended row multiplication from JOINs:

```python
# Check for duplicates in result set
cursor.execute("""
    SELECT user_id, COUNT(*) as cnt
    FROM (
        -- Your query here
        SELECT u.user_id
        FROM users u
        JOIN team_players tp ON u.user_id = tp.user_id
        JOIN teams t ON tp.team_id = t.team_id
    ) subquery
    GROUP BY user_id
    HAVING COUNT(*) > 1
""")

duplicates = cursor.fetchall()
if duplicates:
    print(f"WARNING: {len(duplicates)} users appear multiple times")
    print("Sample duplicates:", duplicates[:5])
```

**Common causes:**
- User on multiple teams (team_players JOIN)
- Multiple relationships (user_relationships)
- Missing DISTINCT keyword

## Relationship Integrity

Check for orphaned records:

```python
# Find team_players with no matching user
cursor.execute("""
    SELECT COUNT(*)
    FROM team_players tp
    LEFT JOIN users u ON tp.user_id = u.user_id
    WHERE u.user_id IS NULL
""")
orphans = cursor.fetchone()[0]

if orphans > 0:
    print(f"WARNING: {orphans} team_players records have no matching user")
```

## Cross-Source Consistency

When using both MySQL and Redshift, verify consistency:

```python
# MySQL count
mysql_cursor.execute("""
    SELECT COUNT(DISTINCT acting_user_id)
    FROM tracked_actions
    WHERE creation_time >= %s AND creation_time < %s
""", (start_date, end_date))
mysql_count = mysql_cursor.fetchone()[0]

# Redshift count
redshift_cursor.execute("""
    SELECT COUNT(DISTINCT acting_user_id)
    FROM tracedb.tracked_actions
    WHERE creation_time >= %s AND creation_time < %s
""", (start_date, end_date))
redshift_count = redshift_cursor.fetchone()[0]

# Compare
diff = abs(mysql_count - redshift_count)
if diff > 0:
    print(f"WARNING: MySQL ({mysql_count}) vs Redshift ({redshift_count}) differ by {diff}")
```

**Note:** Small differences may be expected due to replication lag.

## Business Logic Assertions

Validate that business rules hold:

```python
# Active members should have NULL leave_time
cursor.execute("""
    SELECT COUNT(*)
    FROM team_players
    WHERE leave_time IS NOT NULL
    AND leave_time > NOW()
""")
future_leaves = cursor.fetchone()[0]

if future_leaves > 0:
    print(f"WARNING: {future_leaves} players have future leave dates")

# Validate role flags
cursor.execute("""
    SELECT COUNT(*)
    FROM team_players
    WHERE leave_time IS NULL
    AND is_player = 0 AND is_coach = 0
    AND is_videographer = 0 AND is_follower = 0
""")
no_role = cursor.fetchone()[0]

if no_role > 0:
    print(f"Note: {no_role} active members have no role flags set")
```

## Validation Helper Function

Reusable validation wrapper:

```python
def validate_query_result(cursor, query, params, expected_range=None, check_nulls=None):
    """
    Run a query and validate the results.

    Args:
        cursor: Database cursor
        query: SQL query string
        params: Query parameters
        expected_range: Optional (min, max) tuple for row count
        check_nulls: Optional list of column indices to check for NULLs

    Returns:
        List of rows if valid, raises ValueError if validation fails
    """
    cursor.execute(query, params)
    results = cursor.fetchall()

    # Check row count
    if expected_range:
        min_rows, max_rows = expected_range
        if len(results) < min_rows:
            raise ValueError(f"Too few rows: {len(results)} < {min_rows}")
        if max_rows and len(results) > max_rows:
            raise ValueError(f"Too many rows: {len(results)} > {max_rows}")

    # Check for NULLs
    if check_nulls and results:
        for col_idx in check_nulls:
            null_count = sum(1 for row in results if row[col_idx] is None)
            if null_count > 0:
                raise ValueError(f"Column {col_idx} has {null_count} NULL values")

    return results
```
