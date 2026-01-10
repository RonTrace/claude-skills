# Loading Spinner

ASCII spinner animation for CLI tools. Provides visual feedback during long operations.

## Implementation

```python
import sys
import threading
import time


class Spinner:
    """ASCII loading spinner for CLI operations."""

    def __init__(self, message="Loading"):
        self.spinner_cycle = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.stop_running = threading.Event()
        self.spin_thread = None
        self.message = message
        # Auto-detect if output is a TTY (not piped)
        self.is_tty = sys.stdout.isatty()

    def start(self):
        """Start the spinner in a separate thread."""
        if not self.is_tty:
            # If output is piped, just print the message once
            print(f"{self.message}...")
            return

        self.stop_running.clear()
        self.spin_thread = threading.Thread(target=self._spin)
        self.spin_thread.daemon = True
        self.spin_thread.start()

    def _spin(self):
        """The spinning animation loop."""
        i = 0
        while not self.stop_running.is_set():
            sys.stdout.write(f'\r{self.spinner_cycle[i % len(self.spinner_cycle)]} {self.message}...')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def stop(self):
        """Stop the spinner and clear the line."""
        if not self.is_tty:
            return

        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()
            sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
            sys.stdout.flush()
```

## Usage Examples

### Basic Usage
```python
spinner = Spinner("Loading data")
spinner.start()
# ... perform some operation ...
time.sleep(2)
spinner.stop()
print("Done!")
```

### Database Connection
```python
spinner = Spinner("Connecting to database")
spinner.start()
connection = get_mysql_connection()
spinner.stop()
```

### Multiple Operations
```python
operations = [
    ("Fetching users", fetch_users),
    ("Processing data", process_data),
    ("Generating report", generate_report)
]

for message, operation in operations:
    spinner = Spinner(message)
    spinner.start()
    result = operation()
    spinner.stop()
```

### With Error Handling
```python
spinner = Spinner("Processing")
spinner.start()
try:
    result = risky_operation()
    spinner.stop()
    print("Success!")
except Exception as e:
    spinner.stop()  # Always stop on error
    print(f"Error: {e}")
    sys.exit(1)
```

## Features

- **TTY Detection**: Automatically switches to simple text when output is piped
- **Threaded**: Doesn't block the main operation
- **Clean Stop**: Clears the spinner line when stopped
- **Daemon Thread**: Won't prevent program exit

## Alternative Spinner Styles

```python
# Classic ASCII
spinner_cycle = ['|', '/', '-', '\\']

# Dots
spinner_cycle = ['.  ', '.. ', '...', ' ..', '  .', '   ']

# Arrows
spinner_cycle = ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙']

# Growing bar
spinner_cycle = ['[    ]', '[=   ]', '[==  ]', '[=== ]', '[====]', '[ ===]', '[  ==]', '[   =]']
```

## Best Practices

1. **Descriptive messages**: Tell the user what's happening
   ```python
   # Good
   Spinner("Fetching user activity from database")

   # Bad
   Spinner("Loading")
   ```

2. **Always stop in finally**:
   ```python
   spinner.start()
   try:
       do_work()
   finally:
       spinner.stop()
   ```

3. **Group related quick operations**:
   ```python
   # One spinner for multiple quick operations
   spinner = Spinner("Initializing")
   spinner.start()
   config = load_config()
   logger = setup_logging()
   spinner.stop()
   ```

4. **Separate spinners for distinct phases**:
   ```python
   # Phase 1
   spinner = Spinner("Loading users")
   spinner.start()
   users = load_users()
   spinner.stop()

   # Phase 2
   spinner = Spinner("Processing activities")
   spinner.start()
   activities = process_activities(users)
   spinner.stop()
   ```
