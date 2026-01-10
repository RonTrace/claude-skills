# Advanced Analysis Patterns

## Cross-Category Analysis

### Determining Home vs Away Team Affinity

`target_team_id` is often NOT populated for click actions. To determine team affinity:

1. **For Search clicks:** `target_team_id` is NULL - cannot determine from Search actions alone
2. **For Landing Page:** Use `Home Player Selected` vs `Away Player Selected` action_names
3. **Alternative:** Join `target_game_id` to `games.home_team_id` and compare

```python
def get_team_affinity(session_actions):
    """Determine if user engaged with home or away team."""
    for action in session_actions:
        if action['action_name'] == 'Home Player Selected':
            return 'home'
        elif action['action_name'] == 'Away Player Selected':
            return 'away'
    return None
```

**Note:** `Player Selected` fires alongside `Home/Away Player Selected` - they are NOT mutually exclusive.

---

### Detecting Authentication Status Across a Session

A user may start anonymous and sign in during the same session:

```python
def get_session_auth_status(session_actions):
    """
    Returns: 'never_signed_in', 'signed_in_not_subscribed', or 'signed_in_subscribed'
    """
    user_id = None
    was_ever_subscribed = False

    for action in session_actions:
        if action['acting_user_id']:
            user_id = action['acting_user_id']
        if action['was_subscribed']:
            was_ever_subscribed = True

    if user_id is None:
        return 'never_signed_in'
    elif was_ever_subscribed:
        return 'signed_in_subscribed'
    else:
        return 'signed_in_not_subscribed'
```

**Important:** Looking only at a single category shows ~100% anonymous, which is misleading.

---

### Entry Point Classification

```python
def classify_entry_point(session_actions):
    """Returns: 'search', 'landing_page', or None"""
    if not session_actions:
        return None

    sorted_actions = sorted(session_actions, key=lambda x: x['creation_time'])
    first_action = sorted_actions[0]

    if first_action['action_category'] == 'Search':
        return 'search'
    elif (first_action['action_category'] == 'Landing Page' and
          first_action['action_name'] == 'Landing Page Open'):
        return 'landing_page'
    return None
```

**Typical conversion rates by entry point:**
- Search entry: ~0.4% signup rate
- Landing Page entry: ~1.6% signup rate

---

## Multi-Category Session Analysis

Build session objects that track metrics across categories:

```python
from collections import defaultdict

def build_session_metrics(rows):
    """Build comprehensive session metrics from multi-category data."""
    sessions = defaultdict(lambda: {
        'actions': [],
        'entry_type': None,
        'acting_user_id': None,
        'was_subscribed': False,
        'has_signup': False,
        'has_payment': False,
        'has_video': False,
        'team_affinity': None,
    })

    # Group by tracking_code
    for row in rows:
        sessions[row['tracking_code']]['actions'].append(row)

    # Process each session
    for tc, session in sessions.items():
        session['actions'].sort(key=lambda x: x['creation_time'])

        # Entry point from first action
        first = session['actions'][0]
        if first['action_category'] == 'Search':
            session['entry_type'] = 'search'
        elif first['action_category'] == 'Landing Page':
            session['entry_type'] = 'landing_page'

        # Process all actions
        for action in session['actions']:
            if action['acting_user_id']:
                session['acting_user_id'] = action['acting_user_id']
            if action['was_subscribed']:
                session['was_subscribed'] = True
            if action['action_name'] == 'Account Created':
                session['has_signup'] = True
            elif action['action_name'] == 'Payment Success':
                session['has_payment'] = True
            elif action['action_name'] in ('Watched Highlights', 'Watch Recap', 'Full Game'):
                session['has_video'] = True
            if action['action_name'] == 'Home Player Selected':
                session['team_affinity'] = 'home'
            elif action['action_name'] == 'Away Player Selected':
                session['team_affinity'] = 'away'

    return dict(sessions)
```

---

## Fetching Sessions That Touched a Category

Get ALL actions for sessions that interacted with a specific category:

```sql
SELECT ta.tracking_code, ta.action_category, ta.action_name,
       ta.acting_user_id, ta.was_subscribed, ta.creation_time
FROM tracked_actions ta
WHERE ta.creation_time >= %s AND ta.creation_time < %s
  AND ta.tracking_code IS NOT NULL
  AND ta.tracking_code IN (
      SELECT DISTINCT tracking_code FROM tracked_actions
      WHERE creation_time >= %s AND creation_time < %s
        AND action_category = 'Search' AND tracking_code IS NOT NULL
  )
ORDER BY ta.tracking_code, ta.creation_time
```

**Performance notes:**
- 30 days of Search data: ~1.3M events, ~550K sessions, 30-60 seconds
- Always filter by date in BOTH outer query and subquery
