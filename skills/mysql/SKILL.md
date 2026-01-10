---
name: mysql
description: Query Trace MySQL database for operational data. Use when: (1) looking up users, teams, games, divisions, (2) querying tracked_actions for < 7 days, (3) checking subscriptions or team memberships, (4) building tools that need real-time data. Keywords: user lookup, team query, game data, subscription check, roster, division members.
---

# Trace MySQL Database

## Quick Reference

**Key Tables:** `users`, `teams`, `team_players`, `games`, `divisions`, `tracked_actions`, `subscriptions`

**Connection:** Use `common/scripts/connections.py`:
```python
from connections import get_mysql_connection
conn = get_mysql_connection()
cursor = conn.cursor(dictionary=True)
```

## ⚠️ Critical Rules (Memorize These)

1. **Filter tracked_actions by date FIRST** - It's a huge table
2. **NULL leave_time = active** - In team_players, NULL means still on team
3. **Use tracking_code for sessions** - `acting_user_id` is NULL for anonymous users
4. **Use `title` not `name` for teams** - `name` is a URL slug, `title` is the display name
5. **Always filter subscriptions by object_type** - It's a polymorphic table

## Before You Query

Check the reference docs for tables you'll use. Not all tables are fully documented, but important gotchas and business rules ARE captured.

| If your query involves... | Check this first |
|---------------------------|------------------|
| Users, emails, names, families | [tables/users.md](tables/users.md) |
| Teams, rosters, memberships | [tables/teams.md](tables/teams.md) |
| User activity, funnels, sessions | [tables/tracked-actions.md](tables/tracked-actions.md) |
| Subscriptions, payments, equipment | [tables/subscriptions.md](tables/subscriptions.md) |
| Games, video status, quarantine | [tables/games.md](tables/games.md) |

**After checking docs:** If you need to explore undocumented tables or columns, use patterns from [exploration.md](exploration.md).

## When to Use MySQL vs Redshift

| Use MySQL When... | Use Redshift When... |
|-------------------|---------------------|
| Querying operational data | Running large-scale analytics |
| tracked_actions < 7 days | tracked_actions over long periods |
| Need real-time data | Need pre-aggregated metrics |

---

## 📚 Reference Files (Gotchas & Business Rules)

These docs capture important gotchas, edge cases, and business rules. Check them BEFORE querying to avoid common mistakes. For tables not listed here, use [exploration.md](exploration.md).

### Table Documentation

| File | Contains | Read When... |
|------|----------|--------------|
| [tables/users.md](tables/users.md) | `users`, `user_relationships`, dummy user detection | Querying user data or family relationships |
| [tables/subscriptions.md](tables/subscriptions.md) | `subscriptions` table, product types, equipment patterns, metadata JSON | Checking subscription status or equipment owners |
| [tables/teams.md](tables/teams.md) | `teams`, `team_players`, `divisions`, division-team-player chain | Working with rosters or team membership |
| [tables/games.md](tables/games.md) | `games`, `v_games_played`, game status, quarantine values | Querying game data or video processing status |
| [tables/tracked-actions.md](tables/tracked-actions.md) | `tracked_actions` columns, action categories/names, gotchas | Building analytics or funnel analysis |

### Query Patterns
READ these for proven code patterns:

| File | Contains | Read When... |
|------|----------|--------------|
| [patterns/connection.md](patterns/connection.md) | Connection setup, dictionary cursor, cleanup | Setting up database connection |
| [patterns/users.md](patterns/users.md) | User lookup, family network BFS | Finding users or traversing relationships |
| [patterns/queries.md](patterns/queries.md) | Date filtering, aggregation, JOINs | Writing common query types |
| [patterns/sessions.md](patterns/sessions.md) | Session analysis, funnel patterns, tracking_code usage | Analyzing user journeys or conversions |
| [patterns/entities.md](patterns/entities.md) | Division→Team→Player chain, cohort analysis | Working with entity hierarchies |
| [patterns/advanced.md](patterns/advanced.md) | Cross-category analysis, multi-session metrics | Complex funnel or attribution analysis |

---

## Exploration Commands

```sql
DESCRIBE users              -- Table structure
SELECT * FROM users LIMIT 10  -- Sample data
```

See [exploration.md](exploration.md) for more schema discovery techniques.
