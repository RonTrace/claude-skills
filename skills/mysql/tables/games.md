# Game Tables

## games
Game records.

**Common Columns:**
- `game_id` - Primary key
- `home_team_id` - Home team (**determines division attribution**)
- `away_team_id` - Away team
- `date` - Game date (DATE type)
- `approx_start_time` - Approximate start time (**returns as `timedelta`!**)
- `initial_approx_start_time` - Original scheduled start (DATETIME)
- `scheduled_start` - Scheduled start time
- `creation_time` - When game was created
- `created_user_id` - User who created the game
- `status` - 'unprocessed', 'processing', 'processed', 'process_error'
- `quarantine_status` - Error categorization (NULL or 'none' = not quarantined)
- `subtasks_statuses` - JSON blob with detailed processing status
- `is_deleted`, `is_removed` - Soft delete flags
- `sport_type` - Sport type

## ⚠️ GOTCHA: approx_start_time returns as timedelta

MySQL TIME columns come back as Python `timedelta`, not `time`:
```python
from datetime import datetime, time, timedelta

def get_scheduled_start(game):
    if game['initial_approx_start_time']:
        return game['initial_approx_start_time']

    if game['approx_start_time'] and game['date']:
        if isinstance(game['approx_start_time'], timedelta):
            total_seconds = int(game['approx_start_time'].total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            time_obj = time(hours, minutes, seconds)
        else:
            time_obj = game['approx_start_time']
        return datetime.combine(game['date'], time_obj)
    return None
```

## Game Status

**Check in this order:**
1. `quarantine_status` - If set and not 'none', game has an error
2. `subtasks_statuses.emails.status` - If 'processed', emails were sent
3. `status` - Basic processing status

**Successful game = all of:**
- `status = 'processed'`
- `quarantine_status IS NULL OR quarantine_status = 'none'`
- `subtasks_statuses.emails.status = 'processed'` (for full success)

## Quarantine Status Values
- `equipment_test` - Equipment test game (not real)
- `lost_client_asked_to_delete` - Client deleted
- `removed_by_trace_staff` - Staff removed
- `duplicate` - Duplicate game

## Equipment Test Games

Equipment owners run test games before filming real ones:
```sql
-- Equipment test games
SELECT game_id FROM games WHERE quarantine_status = 'equipment_test'

-- Real games (exclude tests)
SELECT game_id FROM games
WHERE (quarantine_status IS NULL OR quarantine_status = 'none' OR quarantine_status = '')
```

## Common Queries

```sql
-- Upcoming games
SELECT game_id, home_team_id, date
FROM games
WHERE date >= CURDATE() AND is_deleted = 0 AND is_removed = 0

-- Games by division
SELECT g.game_id, g.date, g.status, dt.division_id
FROM games g
INNER JOIN division_teams dt ON g.home_team_id = dt.team_id
WHERE dt.division_id = %s AND g.date >= %s

-- Advance planning analysis
SELECT game_id,
    TIMESTAMPDIFF(HOUR, creation_time, scheduled_start) as hours_in_advance
FROM games WHERE scheduled_start IS NOT NULL
```

---

## v_games_played
View with processed game information.

```sql
SELECT * FROM v_games_played WHERE status = 'processed' AND date >= %s
```

---

## game_video_info
Video file information.

**Detect multicam games:**
```sql
SELECT game_id FROM game_video_info
GROUP BY game_id
HAVING SUM(CASE WHEN file_mode = 'side' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN file_mode = 'main' THEN 1 ELSE 0 END) > 0
```

---

## roster_validation_jobs
Equipment owner onboarding validation. **Introduced October 2025.**

**Columns:**
- `owner_user_id` - Equipment owner
- `division_id` - Division
- `passing_team_id` - Team that passed validation
- `roster_check` - 1 if passed
- `duplicate_camera_check` - 1 if passed

```sql
-- Equipment owners who passed both checks
SELECT owner_user_id, passing_team_id
FROM roster_validation_jobs
WHERE roster_check = 1 AND duplicate_camera_check = 1
```
