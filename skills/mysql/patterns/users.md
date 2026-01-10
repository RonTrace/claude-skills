# User Query Patterns

## User Lookup by Email
```python
def get_user_id_by_email(connection, email):
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None
```

## User Lookup by Email or ID
```python
def get_user(connection, identifier):
    cursor = connection.cursor(dictionary=True)
    if '@' in str(identifier):
        cursor.execute("SELECT * FROM users WHERE email = %s", (identifier,))
    else:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (identifier,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

## Name Coalescing
```python
cursor.execute("""
    SELECT
        user_id, email,
        COALESCE(CONCAT(first_name, ' ', last_name), name) as display_name
    FROM users WHERE user_id = %s
""", (user_id,))
```

---

# Family Network Patterns

## Bidirectional Relationship Query
```python
def get_direct_relations(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT related_user_id FROM user_relationships WHERE user_id = %s
        UNION
        SELECT user_id FROM user_relationships WHERE related_user_id = %s
    """, (user_id, user_id))
    return [row[0] for row in cursor.fetchall()]
```

## BFS Family Network (Performance Optimized)
Recursive CTEs can be slow. Use iterative BFS instead:

```python
def get_family_network(connection, user_id, max_depth=2):
    """Get all family members up to max_depth hops away."""
    family_members = {}
    to_process = [(user_id, 0)]

    while to_process:
        current_id, depth = to_process.pop(0)
        if current_id in family_members or depth > max_depth:
            continue

        family_members[current_id] = depth
        relations = get_direct_relations(connection, current_id)
        for related_id in relations:
            if related_id not in family_members:
                to_process.append((related_id, depth + 1))

    return family_members
```
