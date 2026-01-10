# Connection & Cursor Patterns

## Basic Connection
```python
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

load_dotenv()

def get_mysql_connection():
    try:
        connection = connect(
            host=os.getenv('MYSQL_HOST'),
            port=3306,
            database=os.getenv('MYSQL_DATABASE'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        sys.exit(1)
```

## Dictionary Cursor (Named Access)
```python
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT user_id, email FROM users WHERE user_id = %s", (user_id,))
result = cursor.fetchone()
print(result['email'])  # Access by column name
```

## Cleanup Pattern
```python
connection = get_mysql_connection()
try:
    cursor = connection.cursor(dictionary=True)
    # ... queries ...
finally:
    cursor.close()
    connection.close()
```

## Batch Query with IN Clause
```python
def get_users_by_ids(connection, user_ids):
    if not user_ids:
        return []

    cursor = connection.cursor(dictionary=True)
    placeholders = ', '.join(['%s'] * len(user_ids))
    cursor.execute(f"""
        SELECT user_id, email, COALESCE(CONCAT(first_name, ' ', last_name), name) as name
        FROM users
        WHERE user_id IN ({placeholders})
    """, tuple(user_ids))
    return cursor.fetchall()
```
