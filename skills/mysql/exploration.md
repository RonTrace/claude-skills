# Schema Exploration

Use this for:
- Tables NOT documented in Reference Files
- Discovering column values or data distributions
- Validating assumptions about undocumented columns

**Before exploring:** Check if the table has a doc in `tables/`. If it does, read the gotchas there first.

---

## Discovering Schema

### List All Tables
```python
cursor.execute("SHOW TABLES")
for table in cursor.fetchall():
    print(table[0])
```

### Describe Table Structure
```python
cursor.execute("DESCRIBE users")
for col in cursor.fetchall():
    print(f"{col[0]}: {col[1]}")  # Column name: Data type
```

### Find Tables by Name Pattern
```python
cursor.execute("SHOW TABLES LIKE '%user%'")
```

## Sampling Data

### Quick Sample
```python
cursor.execute("SELECT * FROM table_name LIMIT 10")
for row in cursor.fetchall():
    print(row)
```

### Sample with Specific Conditions
```python
# See what data looks like for a specific user
cursor.execute("""
    SELECT * FROM tracked_actions
    WHERE acting_user_id = %s
    LIMIT 20
""", (sample_user_id,))
```

### Random Sample
```python
cursor.execute("SELECT * FROM users ORDER BY RAND() LIMIT 10")
```

## Validating & Testing

For comprehensive validation patterns, see the `testing` skill:

- [validation.md](../testing/validation.md) - NULL checks, distinct values, date ranges, duplicates, totals reconciliation
- [spot-checking.md](../testing/spot-checking.md) - Sample inspection, known record verification
- [checklists.md](../testing/checklists.md) - Pre-query and pre-delivery checklists

**Quick validation checklist:**
1. Check NULLs in key columns
2. Verify date range coverage
3. Confirm distinct values are expected
4. Totals reconcile (sum of parts = whole)
5. Spot-check known records

See also: [When to ask the user](../testing/SKILL.md#when-to-ask-the-user) in the testing skill.

## Exploration Workflow

1. **Start broad, then narrow**
   ```python
   # First: What tables exist?
   cursor.execute("SHOW TABLES")

   # Then: What columns in the relevant table?
   cursor.execute("DESCRIBE tracked_actions")

   # Then: What does the data look like?
   cursor.execute("SELECT * FROM tracked_actions LIMIT 10")

   # Then: What are the distinct values?
   cursor.execute("SELECT DISTINCT action_category FROM tracked_actions")
   ```

2. **Always check counts first**
   ```python
   # Before complex queries, know how much data you're dealing with
   cursor.execute("SELECT COUNT(*) FROM tracked_actions WHERE creation_time >= %s", (start_date,))
   ```

3. **Test with small date ranges**
   ```python
   # Start with 1 day, not 1 year
   cursor.execute("""
       SELECT * FROM tracked_actions
       WHERE creation_time >= '2025-01-01' AND creation_time < '2025-01-02'
       LIMIT 100
   """)
   ```

4. **Document what you find**
   ```python
   # Add comments about business logic discovered
   # NULL leave_time means active member (verified 2025-01-15)
   # is_player and is_coach can both be true for player-coaches
   ```

5. **⚠️ STOP: Should this be in the skills?**

   After discovering something new, ask yourself:
   - Did I find a table not documented in `tables.md`?
   - Did I learn a business rule not in `business-logic.md`?
   - Did I hit a gotcha that would trip up future queries?

   If YES → **Immediately offer to update the skill.** Don't wait until the end.

   ```
   "I discovered that the `game_livestreams` table tracks live streaming data.
   This isn't documented in tables.md. Would you like me to add it?"
   ```

## Red Flags to Watch For

See [testing SKILL.md](../testing/SKILL.md#red-flags) for the full list. Quick reference:

- **Unexpectedly low/high counts** - Filter too restrictive or JOINs duplicating
- **All NULLs** - Column deprecated or conditionally populated
- **Dates in the future** - Data quality issue
- **Negative IDs** - Bug in the query

## Business Logic & Gotchas

### Entity State Rules

**Users:**
- No direct "active" column - activity determined through tracked_actions
- Users can be on multiple teams simultaneously
- Role flags (is_player, is_coach, etc.) can ALL be true at once

**Teams:**
- Active teams = teams with recent games or active players
- `leave_time IS NULL` means player is currently on the team
- Teams belong to divisions via `division_teams`

**Divisions:**
- Active: `content_access IN ('auto_allowed', 'manual_allowed')`
- Inactive: any other content_access value
- `num_subs` = count of subscriptions in the division
- Division owners found via `division_members WHERE is_owner = 1`

**Games:**
- Check `quarantine_status` FIRST - if set (and not 'none'), game has an error
- `is_deleted = 0 AND is_removed = 0` for valid games
- `status = 'processed'` for games with video ready
- `subtasks_statuses` is JSON - parsing is slow, avoid in bulk queries

### Relationship Gotchas

**Division → Team → Player chain:**
- Users don't directly belong to divisions
- Must go: division_teams → team_players → users
- Or use: division_members for division owners only

**Tracked Actions to Divisions:**
Three different paths depending on the action:
1. `target_division_id` - Action directly on division
2. `target_team_id` → `division_teams` - Action on team
3. `acting_user_id` → `team_players` → `division_teams` - User's action

### Performance Gotchas

**tracked_actions is HUGE:**
- ALWAYS filter by `creation_time` first
- Date filter should be in the WHERE clause, not HAVING
- Consider using Redshift for queries spanning months

**Batch processing:**
- Large IN clauses (1000+ items) can timeout
- Use batch sizes of 50-100 for safety
- Consider temp tables for very large sets

**JSON parsing:**
- `subtasks_statuses` is JSON - parsing in Python is slow
- For bulk analysis, use SQL CASE statements on `status` field instead
- Only parse JSON when you need specific subtask details

### Common Cohort Definitions

**Game Cohorts:** Teams grouped by total games played
- Cohort 1: 1 game, Cohort 2: 2 games, ..., Cohort 7: 7+ games

**Division Activity Flags (from tracked_actions):**
- `owner_onboarding` - Any Owner Onboarding Flow action
- `finished_onboarding` - Completed "Download App" step
- `added_players_onboarding` - Players added during onboarding
- `added_players_team_page` - Players added from team page
- `bot_contacted` - Bot contacted division
- `lock_games_modal` - Interacted with lock games modal

### Database Split (MySQL vs Redshift)

| Data Type | Use MySQL | Use Redshift |
|-----------|-----------|--------------|
| User/team/game metadata | Yes | No |
| tracked_actions (small date range) | Yes | Possible |
| tracked_actions (large date range) | No | Yes |
| Pre-aggregated metrics | No | Yes (dbt_prod tables) |
| Division game history stats | No | Yes (flex_watch_divisions_over_games) |
