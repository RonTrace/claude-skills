# Subscriptions Table

**Polymorphic table** - `object_type` determines what `object_id` references.

## Common Columns
- `object_type` - 'user', 'team', or 'division'
- `object_id` - user_id, team_id, or division_id depending on object_type
- `paying_user_id` - The user who pays for this subscription
- `product_type` - Product category (see below)
- `quantity` - Number of subscription units (always multiply by this!)
- `include_equipment` - Boolean (0/1) if subscription includes equipment
- `status` - 'active', 'trialing', 'canceled', 'expired', etc.
- `creation_time` - Subscription start
- `expiration_date` - When subscription expires
- `metadata` - JSON with additional data (team_id, shipping address, etc.)

## Product Types
| Product | MySQL (`product_type`) | Redshift dbt (`product_category`) |
|---------|------------------------|-----------------------------------|
| PlayerFocus Pro | `flex_watch_pro` | `playerfocus_pro` |
| PlayerFocus Basic | `flex_basic_v2`, `flex_watch_focus` | `playerfocus_basic` |
| Other | `trace`, `traceid`, `flex`, `flex_basic`, `flex_playerfocus`, `flex_club`, `equipment` | varies |

## Critical Rules

**1. Always filter by object_type:**
```sql
SELECT * FROM subscriptions
WHERE object_type = 'user' AND object_id = %s
```

**2. Always multiply by quantity:**
```python
total_subs += sub['quantity'] or 1
```

## Equipment Subscriptions

Equipment can be acquired two ways:
1. **`product_type = 'equipment'`** - Standalone equipment purchase
2. **`include_equipment = 1`** - Bundled with personal subscription

```sql
-- All subscriptions that include equipment
SELECT * FROM subscriptions
WHERE product_type = 'equipment' OR include_equipment = 1
```

## Metadata JSON Field

Equipment subscriptions store onboarding data in `metadata`:
```json
{
  "team_id": "683048",
  "shipping": {"city": "Boston", "state": "MA", ...},
  "duration": "year",
  "plan_type": "family"
}
```

```sql
SELECT paying_user_id,
    JSON_EXTRACT(metadata, '$.team_id') as team_id,
    JSON_EXTRACT(metadata, '$.shipping.city') as city
FROM subscriptions
WHERE (product_type = 'equipment' OR include_equipment = 1)
```

## ⚠️ GOTCHA: Equipment Owner Subscriptions Have No metadata.team_id

Equipment owner subscriptions often have **NO `metadata.team_id`**. Filtering by `metadata->>'team_id'` misses them.

**Wrong:**
```sql
SELECT * FROM subscriptions WHERE JSON_EXTRACT(metadata, '$.team_id') = '12345'
```

**Correct - Join through team_players:**
```sql
SELECT DISTINCT s.*
FROM subscriptions s
INNER JOIN team_players tp ON s.paying_user_id = tp.user_id
WHERE tp.team_id IN (...)
```

**Best - Use Redshift dbt table:**
`dbt_prod.subscription_item_associations_extended` handles this correctly.
