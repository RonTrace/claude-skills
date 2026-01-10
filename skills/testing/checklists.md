# Validation Checklists

Formal checklists to ensure analysis quality at each stage.

## Pre-Query Checklist

Run through these before writing complex queries:

- [ ] **Understand data volume** - Run `SELECT COUNT(*)` first
- [ ] **Check for NULLs** - Key columns might have unexpected NULLs
- [ ] **Verify date range coverage** - Data exists for your time period
- [ ] **Identify potential duplicates** - Will JOINs multiply rows?
- [ ] **Confirm column meanings** - Ask if any names are ambiguous
- [ ] **Check distinct values** - Understand what values exist

```python
# Quick pre-query check template
def pre_query_check(cursor, table, date_column, key_columns):
    # Volume
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"Total rows: {cursor.fetchone()[0]:,}")

    # Date range
    cursor.execute(f"SELECT MIN({date_column}), MAX({date_column}) FROM {table}")
    print(f"Date range: {cursor.fetchone()}")

    # NULL check
    for col in key_columns:
        cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL")
        nulls = cursor.fetchone()[0]
        if nulls > 0:
            print(f"WARNING: {col} has {nulls} NULLs")
```

## Pre-Delivery Checklist

Complete these before sharing results with stakeholders:

- [ ] **Totals reconcile** - Sum of parts equals the whole
- [ ] **Spot-checked 3+ known records** - Expected values returned
- [ ] **Tested with different date ranges** - Query works across time periods
- [ ] **Edge cases handled** - Empty results, NULLs don't break output
- [ ] **Business logic validated** - User confirmed metric definitions
- [ ] **No duplicates** - JOINs didn't multiply rows
- [ ] **Output format reviewed** - Numbers display correctly
- [ ] **⚠️ Skill improvement offered** - Did you discover anything that should be documented? (table, gotcha, business rule)

```python
def pre_delivery_check(results, expected_total=None, known_records=None):
    """Run pre-delivery validation."""
    issues = []

    # Check totals
    if expected_total and len(results) != expected_total:
        issues.append(f"Row count mismatch: {len(results)} vs expected {expected_total}")

    # Check for empty results
    if not results:
        issues.append("WARNING: Empty result set")

    # Check known records if provided
    if known_records:
        for record in known_records:
            if record not in results:
                issues.append(f"Missing expected record: {record}")

    if issues:
        print("Pre-delivery check FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        return False

    print("Pre-delivery check PASSED")
    return True
```

## Post-Change Checklist

After modifying an existing analysis tool:

- [ ] **Previous results reproducible** - Old output still works
- [ ] **New logic doesn't break existing outputs** - Backwards compatible
- [ ] **Edge cases re-tested** - Changes didn't break edge handling
- [ ] **Performance acceptable** - Query time similar or better
- [ ] **Documentation updated** - Comments reflect changes

```python
def regression_check(old_results, new_results, tolerance=0.01):
    """Compare old and new results for regression."""

    if len(old_results) != len(new_results):
        print(f"WARNING: Row count changed: {len(old_results)} -> {len(new_results)}")
        return False

    differences = 0
    for old, new in zip(old_results, new_results):
        if old != new:
            differences += 1

    diff_rate = differences / len(old_results)
    if diff_rate > tolerance:
        print(f"WARNING: {differences} rows differ ({diff_rate:.1%})")
        return False

    print(f"Regression check PASSED ({differences} minor differences)")
    return True
```

## Data Quality Checklist

For assessing overall data quality:

- [ ] **No orphaned records** - Foreign keys have matching records
- [ ] **Date columns valid** - No future dates (unless expected)
- [ ] **IDs are positive** - No negative or zero IDs
- [ ] **Email format valid** - Emails have @ symbol
- [ ] **Enum values expected** - Status columns have known values
- [ ] **Numeric ranges sensible** - Counts not negative, percentages 0-100

## Analysis Handoff Checklist

When handing off analysis to another person:

- [ ] **Query documented** - Clear comments explaining logic
- [ ] **Parameters documented** - Date ranges, filters explained
- [ ] **Validation steps included** - How to verify results
- [ ] **Known limitations noted** - Edge cases, data gaps
- [ ] **Dependencies listed** - Required .env variables, packages
- [ ] **Sample output included** - Expected format shown

## Quick Reference Card

Print this and keep handy:

```
BEFORE QUERYING:
[ ] COUNT(*) first
[ ] Check NULLs
[ ] Verify dates

BEFORE DELIVERING:
[ ] Totals match
[ ] Spot-checked
[ ] Tested edge cases
[ ] User approved logic
[ ] Skill update offered?

RED FLAGS:
- Unexpected row counts
- All NULLs in column
- Future dates
- Negative IDs
```
