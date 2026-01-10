# User Tables

## users
User account information.

**Common Columns:**
- `user_id` - Primary key
- `email` - User email address
- `name` - Full name (legacy, may be NULL)
- `first_name`, `last_name` - Split name fields (newer)
- `creation_time` - Account creation timestamp

**Name Handling Pattern:**
```sql
SELECT user_id, COALESCE(CONCAT(first_name, ' ', last_name), name) as display_name
FROM users
```

**Dummy User Detection:**

"Dummy" users are placeholder accounts created for children/players who don't have their own email. They have synthetic emails:
```python
DUMMY_PATTERNS = [
    'dummy%@traceup.com',      # e.g., dummy12345@traceup.com
    'web-app%@traceup.com'     # e.g., web-app67890@traceup.com
]

def is_dummy_user(email):
    if not email:
        return False
    return (email.startswith('dummy') and email.endswith('@traceup.com')) or \
           (email.startswith('web-app') and email.endswith('@traceup.com'))
```

```sql
-- Filter OUT dummy users (get real users only)
SELECT * FROM users
WHERE email NOT LIKE 'dummy%@traceup.com'
  AND email NOT LIKE 'web-app%@traceup.com'
```

**Why this matters:** When counting "families" on a roster, dummy users represent children whose PARENT is the actual family. Look up the parent via `user_relationships`.

---

## user_relationships
Family connections between users. **Stored bidirectionally.**

**Common Columns:**
- `user_id` - One side of relationship
- `related_user_id` - Other side of relationship
- `creation_time` - When relationship was created

**IMPORTANT:** Always query both directions:
```sql
SELECT related_user_id FROM user_relationships WHERE user_id = %s
UNION
SELECT user_id FROM user_relationships WHERE related_user_id = %s
```

---

## user_phone_numbers
Phone contact information.

**Common Columns:**
- `user_id` - Foreign key to users
- `number` - Phone number
