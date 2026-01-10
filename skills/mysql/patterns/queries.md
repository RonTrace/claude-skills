# Common Query Patterns

## Date Filtering

### Basic Date Range
```python
cursor.execute("""
    SELECT * FROM tracked_actions
    WHERE creation_time >= %s AND creation_time < %s
""", (start_date, end_date))
```

### Relative Date Parsing
```python
from datetime import datetime, timedelta

def parse_relative_date(date_str):
    """Parse '7d', '2w', '1m', 'today', 'yesterday', or YYYY-MM-DD"""
    date_str = date_str.lower().strip()

    if date_str == 'today':
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif date_str == 'yesterday':
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    elif date_str.endswith('d'):
        days = int(date_str[:-1])
        return datetime.now() - timedelta(days=days)
    elif date_str.endswith('w'):
        weeks = int(date_str[:-1])
        return datetime.now() - timedelta(weeks=weeks)
    elif date_str.endswith('m'):
        months = int(date_str[:-1])
        return datetime.now() - timedelta(days=months*30)
    else:
        return datetime.strptime(date_str, '%Y-%m-%d')
```

---

## Aggregation Patterns

### Count by Category
```python
cursor.execute("""
    SELECT action_category, COUNT(*) as count
    FROM tracked_actions
    WHERE acting_user_id = %s AND creation_time >= %s
    GROUP BY action_category
    ORDER BY count DESC
""", (user_id, start_date))
```

### Daily Counts
```python
cursor.execute("""
    SELECT DATE(creation_time) as date, COUNT(*) as daily_count
    FROM tracked_actions
    WHERE acting_user_id = %s AND creation_time >= %s
    GROUP BY DATE(creation_time)
    ORDER BY date DESC
""", (user_id, start_date))
```

### Window Functions (First Action per User)
```python
cursor.execute("""
    WITH ranked AS (
        SELECT acting_user_id, action_name, creation_time,
            ROW_NUMBER() OVER(PARTITION BY acting_user_id ORDER BY creation_time) as rn
        FROM tracked_actions
        WHERE creation_time >= %s AND creation_time < %s
    )
    SELECT acting_user_id, action_name, creation_time
    FROM ranked WHERE rn = 1
""", (start_date, end_date))
```

---

## JOIN Patterns

### User with Team Info
```python
cursor.execute("""
    SELECT
        u.user_id, u.email,
        t.team_id, t.title as team_name,  -- Use title, not name!
        CASE
            WHEN tp.is_player THEN 'player'
            WHEN tp.is_coach THEN 'coach'
            ELSE 'member'
        END as role
    FROM users u
    JOIN team_players tp ON u.user_id = tp.user_id
    JOIN teams t ON tp.team_id = t.team_id
    WHERE u.user_id = %s AND tp.leave_time IS NULL
""", (user_id,))
```

### Division from User (Indirect)
```python
cursor.execute("""
    SELECT DISTINCT d.division_id, d.title as division_name
    FROM team_players tp
    JOIN division_teams dt ON tp.team_id = dt.team_id
    JOIN divisions d ON dt.division_id = d.division_id
    WHERE tp.user_id = %s AND tp.leave_time IS NULL
""", (user_id,))
```

### Check User Subscription
```python
cursor.execute("""
    SELECT status, creation_time FROM subscriptions
    WHERE object_type = 'user' AND object_id = %s
    ORDER BY creation_time DESC LIMIT 1
""", (user_id,))
```
