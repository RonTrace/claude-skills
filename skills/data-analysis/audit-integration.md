# Audit Integration

Patterns for building auditable analysis. Every analysis should produce artifacts that allow someone to trace how results were derived.

## Query Logging

Wrap database operations to capture audit trail:

```python
import json
from datetime import datetime

AUDIT_LOG = []

def audited_query(cursor, query, params=None, description=None):
    """Execute query with automatic audit logging."""
    start = datetime.now()
    cursor.execute(query, params)
    results = cursor.fetchall()
    elapsed = (datetime.now() - start).total_seconds() * 1000

    AUDIT_LOG.append({
        "timestamp": start.isoformat(),
        "description": description,
        "query": query,
        "params": str(params) if params else None,
        "row_count": len(results),
        "duration_ms": round(elapsed, 2)
    })
    return results

def save_audit_log(filepath="audit_log.json"):
    with open(filepath, 'w') as f:
        json.dump(AUDIT_LOG, f, indent=2)
```

### Usage

```python
# Instead of:
cursor.execute("SELECT COUNT(*) FROM users WHERE status = %s", ('active',))

# Use:
results = audited_query(
    cursor,
    "SELECT COUNT(*) FROM users WHERE status = %s",
    ('active',),
    description="Count active users"
)
```

### Output Example

`audit_log.json`:
```json
[
  {
    "timestamp": "2025-01-10T14:22:01.123456",
    "description": "Count active users",
    "query": "SELECT COUNT(*) FROM users WHERE status = %s",
    "params": "('active',)",
    "row_count": 1,
    "duration_ms": 45.2
  },
  {
    "timestamp": "2025-01-10T14:22:02.234567",
    "description": "Get user details by team",
    "query": "SELECT user_id, email FROM users WHERE team_id = %s",
    "params": "(123,)",
    "row_count": 45,
    "duration_ms": 120.8
  }
]
```

---

## Assumptions Documentation

After the ask-first interview, document all assumptions and definitions in `assumptions.md`:

```markdown
# Assumptions for [Analysis Name]

## Definitions

- **Active user:** User with at least one tracked_action in the last 30 days
- **Test data exclusion:** Games where away_team LIKE '%test%' OR quarantine_status = 'equipment_test'
- **Division owner:** User with is_owner = 1 in division_members table

## Scope

- **Time period:** 2024-10-01 to 2024-12-31
- **Entities included:** All divisions with content_access IN ('auto_allowed', 'manual_allowed')
- **Entities excluded:** Internal test divisions (division_id IN (1, 2, 3))

## Confirmed by

- Stakeholder name on [date]: Confirmed active user definition
- Data team on [date]: Confirmed test data exclusion logic
```

### Why This Matters

Without documented assumptions:
- Someone auditing your work can't verify your logic
- You can't defend your numbers if questioned
- Future analysts might make different assumptions and get different results

---

## Checkpoints

At each major step, log intermediate results in `checkpoints.md`:

```markdown
# Checkpoints for [Analysis Name]

## Step 1: Total users in scope
- **Query:** `SELECT COUNT(*) FROM users WHERE creation_time >= '2024-10-01'`
- **Result:** 45,230 rows
- **Validation:** Expected 40k-50k based on monthly signups (~15k/month)
- **Status:** PASS

## Step 2: Active users (with activity)
- **Query:** `SELECT COUNT(DISTINCT acting_user_id) FROM tracked_actions WHERE creation_time >= '2024-10-01'`
- **Result:** 28,450 users
- **Validation:** ~63% of total users had activity - reasonable
- **Status:** PASS

## Step 3: Users by team
- **Query:** `SELECT team_id, COUNT(*) FROM team_players WHERE leave_time IS NULL GROUP BY team_id`
- **Result:** 12,340 teams, 89,230 memberships
- **Validation:** avg 7.2 members/team - matches expected range (5-10)
- **Status:** PASS

## Step 4: Final aggregation
- **Query:** [complex join query]
- **Result:** 3,450 divisions with activity
- **Validation:** Sum of parts (3,450) matches total from Step 3 filter
- **Status:** PASS
```

### Checkpoint Pattern

For each major step:
1. **Query:** The actual SQL run
2. **Result:** Row count or summary statistic
3. **Validation:** How you know it's reasonable
4. **Status:** PASS/FAIL/NEEDS_REVIEW

---

## Final Deliverables

Before delivering results, ensure these files exist in your project:

```
analysis-project/
├── audit_log.json       # All queries with timing
├── assumptions.md       # Definitions from interview
├── checkpoints.md       # Intermediate validations
├── final_output.csv     # Or dashboard.html, report.json, etc.
└── README.md            # How to reproduce (optional)
```

### Pre-Delivery Checklist

- [ ] `audit_log.json` has entries for all queries run
- [ ] `assumptions.md` documents every definition and scope decision
- [ ] `checkpoints.md` shows validation at each major step
- [ ] All checkpoints show PASS status
- [ ] Final numbers match checkpoint totals
- [ ] Discoveries section lists anything new (or "None")

---

## Reproducing Results

The audit artifacts should allow anyone to:

1. **Understand scope:** Read `assumptions.md` to know what was included/excluded
2. **Trace derivation:** Follow `checkpoints.md` to see how final numbers were calculated
3. **Verify queries:** Use `audit_log.json` to re-run exact queries
4. **Check timing:** See how long each step took in `audit_log.json`

If someone can't reproduce your results from these artifacts, the audit trail is incomplete.
