# Analytics Tables

## tracedb.tracked_actions
Analytics copy of tracked_actions. Same structure as MySQL but optimized for large-scale queries.

**Common Columns:**
- `action_category` - The surface/flow in the app (e.g., 'Landing Page', 'Subscribe Pay Wall')
- `action_name` - Specific action name within that category
- `action_variant` - Variant of action
- `creation_time` - When action occurred
- `acting_user_id` - User who performed action (NULL for anonymous)
- `target_user_id`, `target_team_id`, `target_game_id`, `target_division_id` - Target context
- `tracking_code` - Session identifier (use when `acting_user_id` is NULL)
- `url` - Associated URL

**Key Concepts:**
- `action_category` = App surface/flow ("where in the app")
- `tracking_code` = Session ID for anonymous users

**Example:**
```sql
SELECT
    DATE_TRUNC('week', creation_time) as week,
    COUNT(DISTINCT acting_user_id) as unique_users,
    COUNT(*) as total_actions
FROM tracedb.tracked_actions
WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY DATE_TRUNC('week', creation_time)
ORDER BY week
```

---

## tracedb.divisions
Division information.

**Common Columns:**
- `division_id` - Primary key
- `title` - Division name
- `creation_time` - When created

---

## tracedb.users
User accounts.

**Note:** No `name` column - only `first_name` and `last_name`:
```sql
SELECT user_id, COALESCE(first_name || ' ' || last_name, 'Unknown') as full_name
FROM users
```

---

# Common Query Patterns

## Weekly Aggregation
```sql
SELECT
    DATE_TRUNC('week', creation_time) as week,
    action_category,
    COUNT(*) as count
FROM tracedb.tracked_actions
WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '90 days'
GROUP BY DATE_TRUNC('week', creation_time), action_category
ORDER BY week, count DESC
```

## Monthly Trend
```sql
SELECT
    DATE_TRUNC('month', creation_time) as month,
    COUNT(DISTINCT acting_user_id) as monthly_active_users
FROM tracedb.tracked_actions
WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', creation_time)
```

## Division Activity
```sql
SELECT
    target_division_id,
    DATE_TRUNC('day', creation_time) as day,
    COUNT(DISTINCT acting_user_id) as active_users
FROM tracedb.tracked_actions
WHERE target_division_id IN (...)
AND creation_time >= CURRENT_TIMESTAMP - INTERVAL '30 days'
GROUP BY target_division_id, DATE_TRUNC('day', creation_time)
```

## Date Range Filtering
```sql
-- Last 7 days
WHERE creation_time >= CURRENT_TIMESTAMP - INTERVAL '7 days'

-- Specific date range
WHERE creation_time >= '2025-01-01' AND creation_time < '2025-02-01'

-- Last complete month
WHERE creation_time >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
AND creation_time < DATE_TRUNC('month', CURRENT_DATE)
```
