# tracked_actions Table

**LARGE TABLE - always filter by date first!**

## Common Columns
- `tracked_action_id` - Primary key
- `creation_time` - When action occurred
- `tracking_code` - **Session identifier (VARCHAR 36)** - Works for anonymous AND logged-in users
- `action_category` - The surface/flow in the app (e.g., 'Search', 'Landing Page')
- `action_name` - Specific action (e.g., 'Searched', 'Clicked Game')
- `action_variant`, `action_value`, `action_group` - Action details
- `acting_user_id` - User who performed action (**NULL for anonymous users**)
- `acting_team_id`, `acting_game_id`, `acting_player_id`, `acting_division_id` - Actor context
- `target_user_id`, `target_team_id`, `target_game_id`, `target_player_id`, `target_division_id` - Target context
- `was_trial`, `was_subscribed` - User status at time
- `role` - User role
- `url` - Associated URL
- `campaign`, `crusade` - Marketing attribution
- `device_type` - 'mobile', 'tablet', 'desktop' (can be NULL)

## Key Concepts

**1. tracking_code is your primary session identifier**
- `acting_user_id` only populated when user is **signed in**
- `tracking_code` works for **all visitors** (anonymous + logged in)
- Always use `tracking_code` for funnel/journey analysis

**2. action_category = App Surface/Flow**
Common categories: 'Search', 'Landing Page', 'Subscribe Pay Wall', 'Session', 'Video Page', 'Stats'

**3. Actor vs Target**
- `acting_*` = Who did the action
- `target_*` = What was acted upon

**4. Marketing Attribution**
- `campaign` - Source ('flex-email', 'sms', 'website')
- Most traffic without campaign = organic/direct

## Always Filter by Date
```sql
SELECT * FROM tracked_actions
WHERE creation_time >= %s AND creation_time < %s
AND action_category = 'Landing Page'
```

## Action Names by Category

### Search Category
| Action Name | Description | Volume |
|-------------|-------------|--------|
| `Clicked Game` | Clicked game in results | ~75% |
| `Searched` | Submitted search query | ~19% |
| `Show more` | Load more results | ~1% |

**Note:** Most search sessions start with `Clicked Game` (SEO landing), not `Searched`.

### Landing Page Category
| Action Name | Description |
|-------------|-------------|
| `Landing Page Open` | Opened game landing page |
| `Home Player Selected` | Selected home team player |
| `Away Player Selected` | Selected away team player |
| `Account Created` | New user registered |
| `User Logged In` | User authenticated |

### Subscribe Pay Wall Category
| Action Name | Description |
|-------------|-------------|
| `Payment Success` | Successful payment |
| `Payment Failure` | Payment failed |

### Video Page / Game Recap Categories
| Action Name | Description |
|-------------|-------------|
| `Watched Highlights` | User watched highlights |
| `Watch Recap` | Watched recap video |
| `Full Game` | Watched full game |

## Critical Gotchas

### Video Engagement - Query BOTH Categories
```sql
SELECT tracking_code, action_name FROM tracked_actions
WHERE creation_time >= %s AND (
    (action_category = 'Video Page' AND action_name IN ('Watched Highlights', 'Saved Highlight to Trace iD'))
    OR (action_category = 'Game Recap Landing Page' AND action_name IN ('Watch Recap', 'Full Game'))
)
```

### Session Category is NOT an Entry Point
`Session` category fires at the **same timestamp** as actual entry points. Always exclude:
```sql
SELECT tracking_code, action_category, action_name
FROM tracked_actions
WHERE action_category != 'Session'  -- Exclude visit markers
ORDER BY tracking_code, creation_time
```

### Session-Based vs User-Based Metrics
Same user often has multiple sessions before converting.
- Session-based conversion: ~0.47%
- User-based conversion: ~4.71% (10x higher!)

**Always deduplicate by user for conversion analysis.**

### Anonymous-to-Logged-In Transitions
~48% of sessions start anonymous and later get a user_id.
**TRUE entry point** = First non-Session action, regardless of user_id.

```sql
WITH first_actions AS (
    SELECT tracking_code, action_category, creation_time,
           ROW_NUMBER() OVER (PARTITION BY tracking_code ORDER BY creation_time) as rn
    FROM tracked_actions
    WHERE creation_time >= %s AND action_category != 'Session'
)
SELECT tracking_code, action_category as entry_point
FROM first_actions WHERE rn = 1
```

## Search Query Extraction
Search queries are in `action_value` JSON, not `keywords`:
```python
import json
def extract_search_query(action_value):
    if not action_value:
        return None
    try:
        data = json.loads(action_value)
        return data.get('q', '').strip().lower() if data.get('q') else None
    except:
        return None
```
