# Team Tables

## teams
Team information.

**Common Columns:**
- `team_id` - Primary key
- `name` - **URL slug (NOT the display name)** - e.g., "north-county-fc-2012-boys"
- `title` - **Actual team name** - Use this for display, e.g., "North County FC 2012 Boys"
- `sport_type` - Sport type (soccer, basketball, etc.)

**⚠️ Important:** Always use `title` for team names, not `name`. The `name` column is a URL-safe slug.

---

## team_players
User-team membership. **NULL leave_time = active member.**

**Common Columns:**
- `user_id` - Foreign key to users
- `team_id` - Foreign key to teams
- `is_player`, `is_coach`, `is_videographer`, `is_follower` - Role booleans
- `jersey_number` - Player jersey number
- `creation_time` - When user joined team
- `leave_time` - When user left (**NULL = still active**)

**Role flags can overlap** - A user can be both player AND coach.

```sql
-- Active members only
SELECT * FROM team_players WHERE team_id = %s AND leave_time IS NULL
```

---

## divisions
Division information.

**Common Columns:**
- `division_id` - Primary key
- `title` - Division name
- `content_access` - **Active status**: 'auto_allowed', 'manual_allowed' = active
- `num_subs` - Number of subscriptions
- `creation_time` - When division was created

```sql
-- Active divisions
SELECT division_id, title FROM divisions
WHERE content_access IN ('auto_allowed', 'manual_allowed')
```

---

## division_members
Division membership.

**Common Columns:**
- `division_id` - Foreign key to divisions
- `user_id` - Foreign key to users
- `is_owner` - Boolean, user is division owner

---

## division_teams
Team-to-division mapping.

**Common Columns:**
- `division_id` - Foreign key to divisions
- `team_id` - Foreign key to teams

---

## Division → Team → Player Chain

The most common JOIN pattern for roster analysis:

```
Division ←─ division_teams ─→ Team ←─ team_players ─→ User ←─ user_relationships ─→ Parent
```

**Full chain - Get all roster members for a division:**
```sql
SELECT
    dt.division_id,
    t.team_id,
    t.title as team_name,
    tp.user_id,
    u.email,
    tp.is_player,
    tp.is_coach
FROM division_teams dt
INNER JOIN teams t ON dt.team_id = t.team_id
INNER JOIN team_players tp ON t.team_id = tp.team_id
INNER JOIN users u ON tp.user_id = u.user_id
WHERE dt.division_id = %s
  AND tp.leave_time IS NULL
  AND tp.is_follower = 0
  AND tp.is_active = 1
```

**Count families per division (with dummy user handling):**
```sql
SELECT dt.division_id, COUNT(DISTINCT person_id) as family_count
FROM division_teams dt
INNER JOIN (
    -- Non-dummy players = 1 family each
    SELECT tp.team_id, u.user_id as person_id
    FROM team_players tp
    INNER JOIN users u ON tp.user_id = u.user_id
    WHERE tp.is_active = 1 AND tp.is_follower = 0
      AND u.email NOT LIKE 'dummy%%@traceup.com'
      AND u.email NOT LIKE 'web-app%%@traceup.com'
    UNION ALL
    -- Dummy players: use their parent as the family
    SELECT tp.team_id, ur.related_user_id as person_id
    FROM team_players tp
    INNER JOIN users u ON tp.user_id = u.user_id
    INNER JOIN user_relationships ur ON u.user_id = ur.user_id
    WHERE tp.is_active = 1 AND tp.is_follower = 0
      AND (u.email LIKE 'dummy%%@traceup.com' OR u.email LIKE 'web-app%%@traceup.com')
) families ON dt.team_id = families.team_id
GROUP BY dt.division_id
```
