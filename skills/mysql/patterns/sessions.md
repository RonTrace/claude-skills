# Session & Funnel Analysis Patterns

## CRITICAL: Use tracking_code, Not acting_user_id

`acting_user_id` is NULL for anonymous users. Use `tracking_code` to track all visitors:

```python
# WRONG - misses anonymous users
cursor.execute("""
    SELECT acting_user_id, action_name FROM tracked_actions
    WHERE acting_user_id IS NOT NULL  -- loses most visitors!
""")

# RIGHT - captures all sessions
cursor.execute("""
    SELECT tracking_code, action_name FROM tracked_actions
    WHERE tracking_code IS NOT NULL
""")
```

---

## Performance Pattern: Fetch Once, Group in Python

Complex JOINs on `tracked_actions` by `tracking_code` are very slow (no index).
Fetch all data in one query, group in Python:

```python
from collections import defaultdict

# Single efficient query
cursor.execute("""
    SELECT tracking_code, action_name, campaign
    FROM tracked_actions
    WHERE action_category = 'Search'
      AND creation_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
      AND tracking_code IS NOT NULL
""")
rows = cursor.fetchall()

# Group in Python (fast)
sessions = defaultdict(lambda: {'searched': 0, 'clicked': 0, 'campaign': None})
for row in rows:
    tc = row['tracking_code']
    if row['action_name'] == 'Searched':
        sessions[tc]['searched'] += 1
        if row['campaign']:
            sessions[tc]['campaign'] = row['campaign']
    elif row['action_name'] == 'Clicked Game':
        sessions[tc]['clicked'] += 1

# Analyze
total = len(sessions)
converted = sum(1 for s in sessions.values() if s['clicked'] > 0)
print(f"Conversion rate: {converted/total*100:.1f}%")
```

---

## Funnel Analysis by Campaign

```python
from collections import defaultdict

cursor.execute("""
    SELECT tracking_code, action_name, campaign
    FROM tracked_actions
    WHERE action_category = %s AND creation_time >= %s AND tracking_code IS NOT NULL
""", (category, start_date))

by_campaign = defaultdict(lambda: [0, 0])  # [total, converted]
sessions = defaultdict(lambda: {'start': False, 'end': False, 'campaign': None})

for row in cursor.fetchall():
    tc = row['tracking_code']
    if row['action_name'] == start_action:
        sessions[tc]['start'] = True
        sessions[tc]['campaign'] = row['campaign'] or '(none)'
    elif row['action_name'] == end_action:
        sessions[tc]['end'] = True

for s in sessions.values():
    if s['start']:
        by_campaign[s['campaign']][0] += 1
        if s['end']:
            by_campaign[s['campaign']][1] += 1

for camp, (total, conv) in sorted(by_campaign.items(), key=lambda x: -x[1][0]):
    print(f"{camp}: {conv}/{total} ({conv/total*100:.1f}%)")
```

---

## Session Journey Lookup (Use Sparingly)

Individual session lookups are slow. Only use for samples:

```python
sample_sessions = list(sessions.keys())[:3]

for tc in sample_sessions:
    cursor.execute("""
        SELECT creation_time, action_category, action_name
        FROM tracked_actions
        WHERE tracking_code = %s
        ORDER BY creation_time LIMIT 10
    """, (tc,))
    print(f"\nSession {tc[:20]}:")
    for row in cursor.fetchall():
        print(f"  {row['creation_time']} | {row['action_category']}/{row['action_name']}")
```

---

## Tracked Actions by Category

```python
cursor.execute("""
    SELECT action_name, COUNT(*) as count
    FROM tracked_actions
    WHERE creation_time >= %s AND action_category = %s
    GROUP BY action_name ORDER BY count DESC
""", (start_date, category))
```

---

## Cohort by URL Pattern

```python
cursor.execute("""
    SELECT acting_user_id,
        CASE
            WHEN url LIKE '%:sf_%' THEN 'zoom_access'
            WHEN url LIKE '%TraceCam_%' THEN 'no_zoom_access'
            ELSE 'other'
        END as cohort
    FROM tracked_actions
    WHERE creation_time >= %s AND creation_time < %s
    AND (url LIKE '%:sf_%' OR url LIKE '%TraceCam_%')
""", (start_date, end_date))
```
