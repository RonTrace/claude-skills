# Business Logic Reference

This guide documents key business logic patterns used across Trace data analysis tools. Understanding these patterns is essential for consistent analysis.

---

## Family Counting

**Logic:**
1. Fetch all team members with their relationships (both parents AND children)
2. Forward-pass grouping: For each unassigned member, start a new group
3. Look at subsequent members - if their relatives include this user, assign to same group
4. Count total groups

**Key difference:** Siblings are only grouped together if a parent who is ON THE TEAM links them. Parents not on the team won't unify children.

### Cohort Labels

All methods use the same cohort buckets:

```python
def get_family_cohort(count):
    if count == 0:
        return '0 families'
    elif 1 <= count <= 2:
        return '1-2 families'
    elif 3 <= count <= 4:
        return '3-4 families'
    elif 5 <= count <= 6:
        return '5-6 families'
    else:
        return '7+ families'
```

---

## Game Status Determination

When analyzing game processing status, check these in **priority order** (first match wins):

```python
import json

def get_game_display_status(status, subtasks_statuses_json, quarantine_status):
    """
    Priority order:
    1. Quarantine (highest) - Game was flagged for removal
    2. Sent - Emails were successfully processed
    3. Unprocessed - Game hasn't been processed yet
    4. Processing - Currently being processed
    5. Not Played - Scheduled but game never happened
    6. Error (fallback)
    """

    # 1. Quarantine takes precedence
    if quarantine_status and quarantine_status != 'none':
        return format_quarantine_status(quarantine_status)

    # 2. Check if emails were sent
    subtasks = json.loads(subtasks_statuses_json) if subtasks_statuses_json else {}
    if subtasks.get('emails', {}).get('status') == 'processed':
        return 'sent'

    # 3-4. Check workflow status
    if status == 'unprocessed':
        return 'unprocessed'
    elif status == 'processing':
        return 'processing'
    elif status == 'process_error':
        # 5. Check for "not played" games
        if subtasks.get('capture_app', {}).get('error_code') == 'capture_app_data_not_found':
            return 'not_played'
        return format_quarantine_status(quarantine_status)

    return format_quarantine_status(quarantine_status)
```

### Quarantine Status Mapping

| Raw Value | Display Status |
|-----------|----------------|
| `lost_client_asked_to_delete` | `customer_deleted` |
| `removed_by_trace_staff` | `staff_removed` |
| `equipment_test` | `equipment_test` |
| `video_not_recorded` | `no_video_recorded` |
| `duplicate` | `duplicate` |
| Other/Unknown | `error_general` |

### Expected Sent Rate Calculation

```python
def calculate_expected_sent_rate(status_counts):
    """
    Expected Sent % = Sent / (Total - Excluded)

    Excluded from denominator:
    - error_client_delete (client asked to remove)
    - error_equipment_test (test recordings)
    """
    sent = status_counts.get('sent', 0)
    total = sum(status_counts.values())

    # Exclude these - they're intentional, not failures
    excluded = (
        status_counts.get('error_client_delete', 0) +
        status_counts.get('error_equipment_test', 0)
    )

    denominator = total - excluded
    if denominator > 0:
        return round((sent / denominator) * 100, 1)
    return None
```

---

## Division Cohort Assignment

Divisions are grouped by **total games played** across all time, not games in a specific month:

```python
def get_game_count_cohort(count):
    if count == 0:
        return '0 games'
    elif count == 1:
        return '1 game'
    elif count == 2:
        return '2 games'
    elif count == 3:
        return '3 games'
    elif count == 4:
        return '4 games'
    elif count == 5:
        return '5 games'
    elif count == 6:
        return '6 games'
    else:
        return '7+ games'
```

**Important:** A division's cohort is determined by their TOTAL game count, even when analyzing a specific month. A division with 5 total games will be in the "5 games" cohort when looking at ANY of those games.

---

## Advance Planner Classification

An "advance planner" is a user who schedules games ahead of time:

```python
from datetime import datetime

def is_advance_planner(game_creation_time, scheduled_start, now=None):
    """
    Advance planner criteria:
    1. ANY future game (scheduled after now)
    2. Past games must be scheduled 24+ hours after creation
    """
    if now is None:
        now = datetime.now()

    is_future = scheduled_start > now

    if is_future:
        # Any future game = advance planning
        return True, 'future'

    # Past game: check if it was scheduled 24+ hours in advance
    delta_hours = (scheduled_start - game_creation_time).total_seconds() / 3600
    if delta_hours >= 24:
        return True, 'past_advance'

    return False, None
```

| Game Type | Rule | Reasoning |
|-----------|------|-----------|
| Future games | Any advance time | They're planning ahead by definition |
| Past games | 24+ hours advance | Filters out same-day planners |

---

## Tracked Actions Flags for Onboarding

Common boolean flags for tracking onboarding progress:

| Flag | Query Pattern | What It Means |
|------|---------------|---------------|
| `visited_owner_onboarding` | `action_category = 'Owner Onboarding Flow'` | User started onboarding |
| `finished_owner_onboarding` | `action_name = 'Step Visited: Download App'` | User completed onboarding |
| `added_players_onboarding` | `action_name LIKE '%Players Added%'` (in onboarding) | Added players during onboarding |
| `added_players_team_page` | `action_category = 'Team Page'` + `'%Players Added%'` | Added players from team page |
| `bot_contacted` | `action_category = 'Owner Onboarding Bot'` | Division was contacted by bot |
| `lock_games_modal` | `action_category = 'Lock Games Modal'` | User saw the lock games modal |
| `onboarding_a` / `onboarding_b` | `action_group = 'A'` or `'B'` | A/B test variant |

**Example query for onboarding flags:**
```sql
-- Check if any team member in division visited onboarding
SELECT DISTINCT dt.division_id
FROM division_teams dt
INNER JOIN team_players tp ON dt.team_id = tp.team_id
INNER JOIN tracked_actions ta ON tp.user_id = ta.acting_user_id
WHERE dt.division_id IN (...)
  AND ta.action_category = 'Owner Onboarding Flow'
  AND ta.creation_time >= '2025-06-01'
```

---

## Upload Health Status

Upload health tracks the quality of video uploads from cameras. A game's upload health is determined by checking video file integrity and camera session behavior.

### Status Categories

| Status | Condition | Description |
|--------|-----------|-------------|
| `healthy` | All files good, both A/B initial files present | No issues detected |
| `restart_issues` | Bad files AND `associated_sessions > 1` | Camera restarted during recording |
| `duration_issues` | Bad files but no restart | Video duration problems without restart |
| `missing_initial_files` | Files exist but missing `_001.MP4` | First video chunk not uploaded |
| `no_videos_assigned` | Both cameras have 0 files | No video files at all |

### Video File Quality Check

```sql
-- Expected video file duration: 300000ms (5 minutes)
-- Tolerance: 1000ms (1 second)
CASE
    WHEN ABS(duration_ms - 300000) > 1000 THEN 'bad'
    ELSE 'good'
END AS file_quality

-- First video chunk (_001.MP4) contains sound sync tone
-- Exclude last file from duration checks (often truncated)
```

### Camera Restart Detection

Multiple `associated_sessions` in `camera_metadata` indicates camera restart during recording:

```sql
-- Count associated sessions
CASE
    WHEN NULLIF(json_extract_path_text(camera_metadata, 'game_info_v3', 'associated_sessions'), '') IS NULL
    THEN 0
    ELSE json_array_length(NULLIF(json_extract_path_text(camera_metadata, 'game_info_v3', 'associated_sessions'), ''))
END AS num_associated_sessions

-- > 1 means restart occurred
```

### Battery Shutdown Analysis

```sql
-- Normal shutdown vs crash detection
json_extract_path_text(camera_metadata, 'game_info_v3', 'battery', 'normalOff')  -- 'true' = normal
json_extract_path_text(camera_metadata, 'game_info_v3', 'battery', 'died')       -- 'true' = battery died
```

---

## Product Category Name Mapping

Product types have different names in MySQL vs Redshift. Always use the appropriate names for each database.

| Product | MySQL (`subscriptions.product_type`) | Redshift dbt (`product_category`) |
|---------|--------------------------------------|-----------------------------------|
| PlayerFocus Pro | `flex_watch_pro` | `playerfocus_pro` |
| PlayerFocus Basic | `flex_basic_v2`, `flex_watch_focus` | `playerfocus_basic` |

---

## FbF Division Filtering

FbF (Film by Family) divisions can be identified using the `channels` column in `dbt_prod.flex_watch_divisions_over_games`.

**Filter for FbF (non-Bulk) divisions:**
```sql
WHERE channels LIKE '%FbF%'
  AND channels NOT LIKE '%Bulk%'
```

**FbF Channel Variants:**
When querying subscriptions by channel, be aware of multiple FbF channel types:
- `FbF` (primary)
- `FbF SoccerDotCom`
- `FbF League Camera`

**Always use `LIKE 'FbF%'`** to catch all variants, not exact match `= 'FbF'`.

---

## Cohort Analysis for Time-Based Metrics

When analyzing metrics "by weeks since division creation" (e.g., subscription growth over time), use proper cohort methodology.

### The Correct Pattern

**Step 1: Calculate Division Age**
For each division, calculate how many weeks old it is as of today:
```python
from datetime import date

def get_division_weeks_old(division_creation_time, today=None):
    if today is None:
        today = date.today()
    return (today - division_creation_time.date()).days // 7
```

**Step 2: Filter Cohort by Week**
For week N, only include divisions that have existed for at least N weeks:
```python
def get_eligible_divisions(divisions, week):
    """Only include divisions old enough to have data for this week."""
    return [d for d in divisions if d['weeks_old'] >= week]
```

**Step 3: Filter Metrics to Match Cohort**
**Critical:** Only count metrics from divisions in the eligible cohort:
```python
def get_cumulative_for_week(div_week_data, eligible_div_ids, week):
    """Sum metrics only from eligible divisions."""
    return sum(
        sum(div_week_data[div_id].get(w, 0) for w in range(week + 1))
        for div_id in eligible_div_ids
    )
```

**Step 4: Calculate Correct Average**
```python
avg_per_div = cumulative / len(eligible_divs)
```

### Common Mistake

Counting all subscriptions but dividing by a shrinking cohort inflates the average artificially.

**Wrong:**
```
Week 20: 17,370 cumulative / 1,051 divisions = 16.53 avg/div  # WRONG!
```
(Using all subscriptions but only counting divisions that reached week 20)

**Correct:**
```
Week 20: 5,024 cumulative / 1,051 divisions = 4.78 avg/div   # Correct
```
(Using only subscriptions from divisions that reached week 20)

### Example Output Table Structure
```
Week | New Subs | Divisions | Cumulative | Avg/Div
-----|----------|-----------|------------|--------
  12 |      258 |     3,896 |     16,340 |   4.19
  13 |      209 |     3,811 |     16,249 |   4.26
  14 |      225 |     3,730 |     16,178 |   4.34
```

Note how:
- Divisions drops (later divisions haven't reached this week yet)
- Cumulative also drops (excluding subs from excluded divisions)
- Avg/div increases modestly (older divisions accumulate more subs)

---

## Pre-Division Subscriptions

Subscriptions can be created BEFORE the division they're associated with exists. This happens when:
1. Customer purchases subscription
2. Customer creates division afterward

### How to Handle

Count pre-division subscriptions as "week 0" since they represent the initial subscriber base:

```python
def get_subscription_week_offset(subscription_created, division_creation_time):
    """Calculate which week a subscription belongs to relative to division creation."""
    days_offset = (subscription_created - division_creation_time).days
    week_offset = days_offset // 7

    # Pre-division subscriptions count as week 0
    if week_offset < 0:
        week_offset = 0

    return week_offset
```

### Typical Distribution (Q3 2025 FbF Example)

| Timing | Subscriptions | Divisions |
|--------|---------------|-----------|
| 30+ days before | 151 | 117 |
| 8-30 days before | 37 | 35 |
| 1-7 days before | 54 | 50 |
| Same day | 2,473 | 2,294 |
| 1-7 days after | 1,402 | 731 |
| 8-30 days after | 6,902 | 2,121 |
| 30+ days after | 6,222 | 2,059 |

Most subscriptions happen on or shortly after division creation, but a meaningful portion (~1.4%) precede the division.

---

## Key Gotchas

1. **Only `home_team_id` determines division** - Away games don't count toward division metrics

2. **`is_active = 1` AND `is_follower = 0`** - Standard filter for roster members (excludes fans and inactive)

3. **Division active status** - Check `content_access IN ('auto_allowed', 'manual_allowed')`

4. **TIME columns return timedelta** - MySQL TIME fields come back as Python `timedelta`, not `time` objects

5. **Dummy users need parent lookup** - Don't count dummy users directly; look up their parent via `user_relationships`

6. **Camera ID formats vary** - Always normalize camera IDs:
   - Asset URL: `https://trce.ai/c?12345` → `X12345`
   - Module ID: `CX6630` → `X6630`
   - Pi ID with path: `X6630/module` → `X6630`

7. **Video file duration standard** - Expected 300000ms (5 minutes) with 1000ms tolerance. Last file per camera is often truncated.
