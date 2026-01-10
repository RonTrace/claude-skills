# Validation Failure Examples

Learn to recognize these patterns of failing validation.

## Failure 1: Totals Don't Reconcile

```
Query 1: SELECT COUNT(*) FROM users WHERE created_at >= '2025-01-01'
Result:  1,000

Query 2: SELECT status, COUNT(*) FROM users WHERE created_at >= '2025-01-01' GROUP BY status
Results:
  active:   450
  inactive: 320
  pending:  217
  TOTAL:    987

FAILED - 13 records missing!
```

**Root cause:** 13 users have NULL status. GROUP BY excludes NULLs.
**Fix:** Add `COALESCE(status, 'unknown')` or investigate why status is NULL.

## Failure 2: Unexpected NULL Rate

```
Query: SELECT COUNT(*), COUNT(email), COUNT(phone) FROM users
Results:
  total:       10,000
  with_email:  10,000 (100%)
  with_phone:   5,500 (55%)

Expected phone rate: ~95% (per product team)

FAILED - 40% more NULLs than expected
```

**Root cause:** Recent signup flow changed, phone became optional.
**Fix:** Confirm with stakeholder if this is expected before reporting.

## Failure 3: JOIN Multiplied Rows

```
Query: SELECT u.user_id, u.email FROM users u
       JOIN team_players tp ON u.user_id = tp.user_id
       WHERE tp.leave_time IS NULL

Expected: ~5,000 active users
Result:   ~8,500 rows

FAILED - 70% more rows than expected
```

**Root cause:** Users can be on multiple teams. JOIN creates one row per team membership.
**Fix:** Add `DISTINCT` or `GROUP BY u.user_id` depending on what you need.

## Failure 4: Date Range Mismatch

```
Query: SELECT MIN(created_at), MAX(created_at) FROM tracked_actions
       WHERE created_at >= '2025-01-01' AND created_at < '2025-02-01'

Result:
  earliest: 2025-01-01 00:00:03
  latest:   2025-01-31 23:59:58

Query covering same range shows 0 rows for Jan 15-17.

FAILED - 3 days of data missing
```

**Root cause:** Database maintenance window, data not replicated.
**Fix:** Document gap, adjust date range, or note in analysis.

## Failure 5: Business Logic Violation

```
Query: SELECT team_id, COUNT(*) as player_count
       FROM team_players
       WHERE leave_time IS NULL AND is_active = 1
       GROUP BY team_id

Result: Team 12345 shows 0 players

But: User reports Team 12345 is actively filming games

FAILED - Known active team shows empty roster
```

**Root cause:** `is_active` flag not used consistently; use `is_follower = 0` instead.
**Fix:** Update query to use correct filter, document in skill gotchas.

## How to Handle Failures

1. **STOP** - Don't deliver results with known issues
2. **Investigate** - Find the root cause before proceeding
3. **Document** - Note what you found and how you fixed it
4. **Update skills** - If this is a reusable lesson, add it to the skill
5. **Communicate** - Tell stakeholder about any caveats or data quality issues
