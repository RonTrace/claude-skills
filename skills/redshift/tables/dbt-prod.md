# dbt_prod Schema - Pre-aggregated Metrics

## flex_watch_divisions_over_games
Pre-aggregated division metrics across game buckets. **Use this for division health analysis instead of computing from raw data.**

**Common Columns:**
- `division_id` - Division identifier
- `division_creation_time` - When division was created
- `first_game_date` - Date of division's first game (use for cohort assignment)
- `num_games` - Total number of games
- `max_num_non_dummy_family_ids` - **Juan's family count** (pre-calculated, excludes dummy users)
- `channels` - Acquisition channel ('Bulk' = bulk uploaded, 'FbF' = Film by Family)
- `games_1_5_total_playerfocus_quantity` - PlayerFocus in games 1-5
- `games_6_10_total_playerfocus_quantity` - PlayerFocus in games 6-10
- `games_11_20_total_playerfocus_quantity` - PlayerFocus in games 11-20
- `games_21_40_total_playerfocus_quantity` - PlayerFocus in games 21-40

**FbF Division Filtering:**
```sql
-- FbF (non-Bulk) divisions
WHERE channels LIKE '%FbF%' AND channels NOT LIKE '%Bulk%'

-- All FbF variants (includes FbF, FbF SoccerDotCom, FbF League Camera)
WHERE channels LIKE '%FbF%'
```

**Useful derived columns:**
```sql
SELECT
    division_id,
    CASE WHEN first_game_date IS NOT NULL
         THEN DATE_TRUNC('week', first_game_date::timestamp) END as first_game_week,
    CASE WHEN first_game_date IS NULL OR num_games = 0 THEN 'Not Started' ELSE 'Started' END as game_status,
    CASE WHEN channels = 'Bulk' THEN true ELSE false END as is_bulk,
    max_num_non_dummy_family_ids as num_families
FROM dbt_prod.flex_watch_divisions_over_games
WHERE division_creation_time >= '2025-06-01'
```

---

## subscription_item_associations_extended
**Best table for linking Stripe subscriptions to divisions.** Cleaner than MySQL - no need to join through `team_players`.

**Common Columns:**
- `stripe_subscription_id` - Unique subscription identifier
- `subscription_created` - When the subscription was created
- `default_division_id` - **Direct division attribution!**
- `product_category` - e.g., `playerfocus_pro`, `playerfocus_basic`
- `channel` - e.g., `FbF`, `FbF SoccerDotCom`, `FbF League Camera`
- `quantity` - **Always multiply by this when counting!**

**FbF Channel Variants:**
- `FbF` (primary)
- `FbF SoccerDotCom`
- `FbF League Camera`

**Always use `LIKE 'FbF%'`** to catch all variants:

```sql
-- FbF Subscriptions by Division
SELECT
    stripe_subscription_id, subscription_created,
    default_division_id as division_id, product_category, quantity
FROM dbt_prod.subscription_item_associations_extended
WHERE product_category IN ('playerfocus_pro', 'playerfocus_basic')
  AND channel LIKE 'FbF%'

-- Count subscriptions (respecting quantity)
SELECT
    default_division_id as division_id,
    SUM(quantity) as total_subscriptions
FROM dbt_prod.subscription_item_associations_extended
WHERE channel LIKE 'FbF%'
GROUP BY default_division_id
```

---

## processing_session_locations
Processing sessions with camera, facility, and division context.

**Common Columns:**
- `date` - Session date
- `game_id` - Associated game
- `division_id` - Division identifier
- `processing_session_camera_id` - Camera used
- `processing_session_facility_id` - Facility ID (sub-unit of division)
- `processing_session_status` - Status (e.g., 'processed')

**Weekly Division Usage Summary:**
```sql
WITH base AS (
  SELECT
    DATE_TRUNC('week', "date"::date)::date AS week_start,
    game_id, processing_session_camera_id, processing_session_facility_id
  FROM dbt_prod.processing_session_locations
  WHERE "date"::date BETWEEN DATE '2025-08-04' AND DATE '2025-12-16'
    AND processing_session_status = 'processed'
    AND division_id = :division_id
)
SELECT
  week_start,
  COUNT(game_id) AS total_sessions,
  COUNT(DISTINCT processing_session_camera_id) AS unique_cameras,
  COUNT(DISTINCT processing_session_facility_id) AS unique_facilities
FROM base
GROUP BY 1 ORDER BY 1
```
