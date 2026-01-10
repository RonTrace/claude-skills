# Combining Skills for Complex Analyses

Many analyses require data from multiple sources or multiple skill patterns. This guide shows how to combine them effectively.

## Example 1: User Activity with Family Context

**Goal:** Analyze a user's activity including their family members

**Skills needed:**
- `mysql` - For user_relationships and tracked_actions
- `cli-patterns` - For CLI scaffolding with spinner

**Pattern:**
```python
from spinner import Spinner  # From cli-patterns

def analyze_user_with_family(user_id):
    connection = get_mysql_connection()

    # Step 1: Get family network
    spinner = Spinner("Discovering family network")
    spinner.start()
    family_ids = get_family_members(connection, user_id)  # BFS pattern
    spinner.stop()

    # Step 2: Get activity for all family members
    spinner = Spinner("Loading family activity")
    spinner.start()
    cursor = connection.cursor(dictionary=True)
    placeholders = ', '.join(['%s'] * len(family_ids))
    cursor.execute(f"""
        SELECT acting_user_id, action_category, action_name, COUNT(*) as count
        FROM tracked_actions
        WHERE acting_user_id IN ({placeholders})
        AND creation_time >= %s
        GROUP BY acting_user_id, action_category, action_name
    """, (*family_ids, start_date))
    spinner.stop()

    return cursor.fetchall()
```

## Example 2: Subscription Analysis with Stripe Data

**Goal:** Link Stripe subscription data with Trace user activity

**Skills needed:**
- `stripe` - For Stripe customer data
- `mysql` - For Trace user data
- `cli-patterns` - For CLI scaffolding

**Pattern:**
```python
import stripe
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv('STRIPE_API_KEY')

def analyze_subscriber_engagement(email):
    # Step 1: Get Stripe customer info
    customers = stripe.Customer.list(email=email)
    if not customers.data:
        print(f"No Stripe customer found for {email}")
        return

    customer = customers.data[0]

    # Step 2: Get Trace user info
    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        print(f"No Trace user found for {email}")
        return

    # Step 3: Combine the data
    cursor.execute("""
        SELECT action_category, COUNT(*) as actions
        FROM tracked_actions
        WHERE acting_user_id = %s
        AND creation_time >= %s
        GROUP BY action_category
    """, (user['user_id'], customer.created))  # Since Stripe signup

    return {
        'stripe_customer_id': customer.id,
        'trace_user_id': user['user_id'],
        'activity': cursor.fetchall()
    }
```

## Example 3: Large-Scale Cohort Analysis

**Goal:** Analyze cohorts with millions of rows

**Skills needed:**
- `mysql` - For user/team metadata
- `redshift` - For tracked_actions at scale
- `cli-patterns` - For progress feedback

**Pattern:**
```python
def analyze_large_cohort(division_ids, start_date, end_date):
    # Step 1: Get metadata from MySQL (fast, small tables)
    mysql_conn = get_mysql_connection()
    cursor = mysql_conn.cursor(dictionary=True)

    placeholders = ', '.join(['%s'] * len(division_ids))
    cursor.execute(f"""
        SELECT d.division_id, d.title, COUNT(DISTINCT dm.user_id) as member_count
        FROM divisions d
        JOIN division_members dm ON d.division_id = dm.division_id
        WHERE d.division_id IN ({placeholders})
        GROUP BY d.division_id
    """, tuple(division_ids))
    divisions = cursor.fetchall()
    mysql_conn.close()

    # Step 2: Get activity from Redshift (handles scale)
    redshift_conn = get_redshift_connection()
    cursor = redshift_conn.cursor()

    # Note: Redshift SQL syntax differences!
    cursor.execute(f"""
        SELECT
            target_division_id,
            DATE_TRUNC('week', creation_time) as week,
            COUNT(DISTINCT acting_user_id) as active_users
        FROM tracedb.tracked_actions
        WHERE target_division_id IN ({placeholders})
        AND creation_time >= %s
        AND creation_time < %s
        GROUP BY target_division_id, DATE_TRUNC('week', creation_time)
    """, (*division_ids, start_date, end_date))
    activity = cursor.fetchall()
    redshift_conn.close()

    # Step 3: Combine results
    return merge_metadata_with_activity(divisions, activity)
```

## Example 4: CLI Tool with Dashboard Output

**Goal:** Generate an interactive HTML dashboard from CLI

**Skills needed:**
- `mysql` or `redshift` - For data
- `cli-patterns` - For CLI structure
- `ui` - For HTML generation and UI components

**Pattern:**
```python
#!/usr/bin/env python3
"""
Cohort Dashboard Generator

Usage:
    python generate_dashboard.py --start-date 2025-01-01
"""

import argparse
import json
from data_fetcher import fetch_data  # Reusable data fetcher pattern
from template import generate_html   # HTML template pattern from ui

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-date', required=True)
    args = parser.parse_args()

    # Fetch data using data_fetcher pattern
    spinner = Spinner("Fetching cohort data")
    spinner.start()
    data = fetch_data(start_date=args.start_date)
    spinner.stop()

    # Generate HTML using dashboard patterns
    spinner = Spinner("Generating dashboard")
    spinner.start()
    html = generate_html(data)
    spinner.stop()

    # Write output
    with open('index.html', 'w') as f:
        f.write(html)

    print(f"Dashboard generated: index.html")

if __name__ == "__main__":
    main()
```

## Data Flow Patterns

### Pattern A: Single Source, Simple Output
```
MySQL/Redshift → Transform → Console/CSV
```
Skills: One database skill + cli-patterns

### Pattern B: Multi-Source Analysis
```
MySQL (metadata) ─┐
                  ├─→ Combine → Analysis → Output
Redshift (scale) ─┘
```
Skills: mysql + redshift + cli-patterns

### Pattern C: Full Stack with Visualization
```
Database → Data Fetcher → Transform → HTML Template → Dashboard
```
Skills: Database skill + cli-patterns + ui

### Pattern D: Payment Integration
```
Stripe (billing) ─┐
                  ├─→ Link by email → Combined Analysis
MySQL (users)    ─┘
```
Skills: stripe + mysql + cli-patterns

### Pattern E: Division/Roster Cohort Analysis
```
Redshift (divisions, family counts, first game dates)
                  │
                  ├─→ Get division IDs
                  │
MySQL (status, teams, rosters, tracked_actions)
                  │
                  ├─→ Enrich with real-time data
                  │
                  └─→ Calculate cohorts → Output
```
Skills: redshift + mysql + cli-patterns

**Typical data flow:**
1. **Redshift first** - `flex_watch_divisions_over_games` for pre-aggregated metrics
2. **MySQL enrichment** - Division status, team names, roster counts
3. **MySQL tracked_actions** - Onboarding flags, user behavior
4. **Combine and cohort** - Apply business logic (see [business-logic.md](business-logic.md))

**Example:**
```python
def fetch_division_cohorts():
    # 1. Get aggregated data from Redshift
    redshift_conn = get_redshift_connection()
    divisions = query_flex_watch_divisions(redshift_conn)
    division_ids = list(divisions.keys())

    # 2. Enrich from MySQL
    mysql_conn = get_mysql_connection()
    statuses = get_division_statuses(mysql_conn, division_ids)  # content_access
    teams = get_division_teams(mysql_conn, division_ids)        # team names
    family_counts = count_families(mysql_conn, division_ids)    # real-time roster count
    onboarding_flags = get_onboarding_flags(mysql_conn, division_ids)

    # 3. Combine and calculate cohorts
    for div_id, data in divisions.items():
        data['status'] = statuses.get(div_id, 'inactive')
        data['family_cohort'] = get_family_cohort(family_counts.get(div_id, 0))
        data.update(onboarding_flags.get(div_id, {}))

    return divisions
```

## Best Practices for Combined Analyses

1. **Fetch metadata first** - Small tables from MySQL before large queries from Redshift
2. **Batch lookups** - Use IN clauses instead of individual queries
3. **Close connections promptly** - Don't hold connections while processing
4. **Handle failures gracefully** - One source failing shouldn't crash everything
5. **Log progress** - Use spinners to show which phase is running
6. **Validate at boundaries** - Check data makes sense when combining sources
