---
name: redshift
description: Query Trace Redshift data warehouse for large-scale analytics. Use when: (1) querying tracked_actions for > 7 days, (2) using pre-aggregated dbt_prod tables, (3) MySQL queries timeout, (4) historical trend analysis. Keywords: analytics, historical data, division metrics, camera metadata, subscription attribution, weekly trends.
---

# Trace Redshift Data Warehouse

## ⚠️ CRITICAL: PostgreSQL Syntax (Not MySQL!)

| Wrong (MySQL) | Right (Redshift) |
|---------------|------------------|
| `CONCAT(a, b)` | `a \|\| b` |
| `DATE(ts)` | `DATE_TRUNC('day', ts)` |
| `NOW()` | `CURRENT_TIMESTAMP` |
| `HOUR(ts)` | `EXTRACT(HOUR FROM ts)` |
| `INTERVAL 7 DAY` | `INTERVAL '7 days'` |
| `DATE_SUB(d, INTERVAL 7 DAY)` | `d - INTERVAL '7 days'` |

## Quick Reference

**Connection:** Use `common/scripts/connections.py`:
```python
from connections import get_redshift_connection, get_redshift_dict_cursor
conn = get_redshift_connection()
cursor = get_redshift_dict_cursor(conn)
```

**Key Schemas:**
- `tracedb` - Operational copy (tracked_actions, users, games, hardware)
- `dbt_prod` - Pre-aggregated metrics (division health, subscription attribution)
- `hubspot` - CRM deals linked to divisions
- `shipstation` - Shipping records

## When to Use Redshift vs MySQL

| Use Redshift When... | Use MySQL When... |
|---------------------|-------------------|
| Millions of tracked_actions rows | Small operational queries |
| Long date ranges (months/years) | Short date ranges (days) |
| Pre-aggregated metrics needed | Real-time data needed |
| MySQL query times out | Performance is acceptable |

## Before You Query

Check the reference docs for tables you'll use. Not all tables are fully documented, but important gotchas and business rules ARE captured.

| If your query involves... | Check this first |
|---------------------------|------------------|
| User activity, funnels | [tables/analytics.md](tables/analytics.md) |
| Division health, subscription attribution | [tables/dbt-prod.md](tables/dbt-prod.md) |
| Camera metadata, hardware tracking | [tables/camera.md](tables/camera.md) |
| CRM deals, shipping records | [tables/integrations.md](tables/integrations.md) |

**After checking docs:** If you need to explore undocumented tables or columns, use patterns from [exploration.md](exploration.md).

---

## 📚 Reference Files (Gotchas & Business Rules)

These docs capture important gotchas, edge cases, and business rules. Check them BEFORE querying to avoid common mistakes. For tables not listed here, use [exploration.md](exploration.md).

| File | Contains | Read When... |
|------|----------|--------------|
| [tables/analytics.md](tables/analytics.md) | `tracked_actions`, `divisions`, `users`, common aggregation patterns | Building analytics or user activity queries |
| [tables/dbt-prod.md](tables/dbt-prod.md) | `flex_watch_divisions_over_games`, `subscription_item_associations_extended`, FbF channel filtering | Analyzing division health or subscription attribution |
| [tables/camera.md](tables/camera.md) | `game_resources`, `hardware_assets`, `case_sessions`, JSON parsing patterns | Working with camera metadata or hardware tracking |
| [tables/integrations.md](tables/integrations.md) | `hubspot.deals`, `shipstation.shipments` | Querying CRM or shipping data |

---

## Critical Gotchas

1. **No dictionary cursor by default** - Use `get_redshift_dict_cursor(conn)`
2. **Case sensitivity** - Redshift lowercases identifiers unless quoted
3. **No `name` column in users** - Only `first_name` and `last_name`
4. **Schema required** - Always prefix tables (e.g., `tracedb.tracked_actions`)
5. **Transactions** - Set `autocommit = True` to avoid lock issues

## Camera ID Normalization

Camera IDs appear in multiple formats. Always normalize:

```sql
-- asset_id URL: 'https://trce.ai/c?12345' → 'X12345'
CONCAT('X', SUBSTRING(asset_id FROM POSITION('c?' IN asset_id) + 2))

-- module prefix: 'CX6630' → 'X6630'
CASE WHEN LEFT(camera_id, 1) = 'C' THEN SUBSTRING(camera_id, 2) ELSE camera_id END

-- path format: 'X6630/module' → 'X6630'
SPLIT_PART(camera_pi_id, '/', 1)
```

---

## Exploration

See [exploration.md](exploration.md) for schema discovery techniques.

```sql
-- List tables in schema
SELECT table_name FROM information_schema.tables WHERE table_schema = 'tracedb'

-- Describe a table
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'tracked_actions'
```
