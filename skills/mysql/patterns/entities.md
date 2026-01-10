# Entity Relationship Patterns

## Division → Teams → Players (Full Chain)

```python
cursor.execute("""
    SELECT
        dt.division_id, dt.team_id,
        t.title as team_name,  -- Use title, not name!
        tp.user_id, u.email
    FROM division_teams dt
    INNER JOIN teams t ON dt.team_id = t.team_id
    INNER JOIN team_players tp ON dt.team_id = tp.team_id
    INNER JOIN users u ON tp.user_id = u.user_id
    WHERE dt.division_id IN (%s) AND tp.leave_time IS NULL
""", (division_id,))
```

## Division → Games (via Teams)

```python
cursor.execute("""
    SELECT
        dt.division_id, g.game_id, g.date, g.status,
        t.title as team_name
    FROM division_teams dt
    INNER JOIN games g ON dt.team_id = g.home_team_id
    INNER JOIN teams t ON dt.team_id = t.team_id
    WHERE dt.division_id = %s AND g.date >= %s AND g.is_deleted = 0
    ORDER BY g.date
""", (division_id, start_date))
```

## Division Owner Contact Info

```python
cursor.execute("""
    SELECT
        dm.division_id, u.user_id, u.email,
        u.first_name, u.last_name,
        upn.number as phone
    FROM division_members dm
    INNER JOIN users u ON dm.user_id = u.user_id
    LEFT JOIN user_phone_numbers upn ON u.user_id = upn.user_id
    WHERE dm.division_id = %s AND dm.is_owner = 1
""", (division_id,))
```

## Tracked Actions → Division (via Team Players)

```python
cursor.execute("""
    SELECT DISTINCT dt.division_id
    FROM division_teams dt
    INNER JOIN team_players tp ON dt.team_id = tp.team_id
    INNER JOIN tracked_actions ta ON tp.user_id = ta.acting_user_id
    WHERE dt.division_id IN (%s)
    AND ta.action_category = %s AND ta.creation_time >= %s
""", (division_ids, category, start_date))
```

## Tracked Actions → Division (via target columns)

```python
# Direct division reference
cursor.execute("""
    SELECT DISTINCT target_division_id as division_id
    FROM tracked_actions
    WHERE target_division_id IN (%s) AND action_category = %s
""", (division_ids, category))

# Via team reference
cursor.execute("""
    SELECT DISTINCT dt.division_id
    FROM division_teams dt
    INNER JOIN tracked_actions ta ON dt.team_id = ta.target_team_id
    WHERE dt.division_id IN (%s) AND ta.action_category = %s
""", (division_ids, category))
```

---

# Cohort Analysis Patterns

## Team Cohorts by Game Count

```python
cursor.execute("""
    SELECT home_team_id, COUNT(*) as game_count,
        CASE WHEN COUNT(*) >= 7 THEN '7+' ELSE CAST(COUNT(*) AS CHAR) END as cohort
    FROM games
    WHERE date >= %s AND is_deleted = 0
    GROUP BY home_team_id
""", (start_date,))
```

## Division Cohorts by Game Count

```python
cursor.execute("""
    SELECT dt.division_id, COUNT(DISTINCT g.game_id) as game_count
    FROM division_teams dt
    LEFT JOIN games g ON dt.team_id = g.home_team_id
        AND g.date >= %s AND g.is_deleted = 0
    WHERE dt.division_id IN (%s)
    GROUP BY dt.division_id
""", (start_date, division_ids))
```

## Advance Planners (Games Created 24+ Hours Ahead)

```python
cursor.execute("""
    SELECT dm.user_id, u.email, COUNT(*) as advance_games
    FROM games g
    INNER JOIN division_teams dt ON g.home_team_id = dt.team_id
    INNER JOIN division_members dm ON dt.division_id = dm.division_id
    INNER JOIN users u ON dm.user_id = u.user_id
    WHERE g.scheduled_start IS NOT NULL
    AND TIMESTAMPDIFF(HOUR, g.creation_time, g.scheduled_start) >= 24
    AND g.date >= %s AND dm.is_owner = 1
    GROUP BY dm.user_id
    HAVING COUNT(*) >= 3
""", (start_date,))
```
