# Standard Workflow for Building Analysis Tools

## Quick Navigation

| Phase | Description |
|-------|-------------|
| [Phase 0: Project Setup](#phase-0-project-setup) | Folder structure, .env handling, .gitignore |
| [Phase 1: Requirements](#phase-1-requirements-gathering) | Clarify the question before coding |
| [Phase 2: Discovery](#phase-2-data-discovery) | Explore schema, sample data, validate assumptions |
| [Phase 3: Build Connection](#phase-3-build-the-connection-layer) | Standard CLI tool structure |
| [Phase 4: Build Incrementally](#phase-4-build-incrementally) | Start simple, add complexity |
| [Phase 5: Testing](#phase-5-testing--validation) | Validate before delivery |
| [Phase 6: Output](#phase-6-output-formatting) | Console, CSV, HTML, JSON options |

---

## Phase 0: Project Setup

**Before writing any code, set up a clean project structure:**

### Folder Structure
```
analysis-project-name/
├── .env                    # Environment variables (DO NOT COMMIT)
├── .env.example            # Template showing required vars (safe to commit)
├── .gitignore              # Must include .env
├── final_script.py         # Final polished script only
├── dashboard.html          # Final output only (if applicable)
├── README.md               # Optional: document findings
├── data/                   # All data files (JSON, CSV, etc.)
│   └── output.json
└── work/                   # All exploratory/temp/versioned files
    ├── explore_schema.py
    ├── test_query.py
    ├── dashboard_v1.html
    ├── dashboard_v2.html
    └── ...
```

### Key Rules
1. **Root stays clean** - Only final, production-ready files in the project root
2. **No versioned files in root** - Files like `_v2`, `_old`, `_backup` belong in `work/`
3. **Data files go in `data/`** - JSON, CSV, and other generated data
4. **Work files go in `work/`** - Drafts, experiments, intermediate versions
5. **Always have `.env` in `.gitignore`** - Never commit credentials

### Environment File Rules

**Credentials are sensitive - ALWAYS ask the user before taking action.**

#### When No .env File Exists

If `.env` does not exist in the project directory, you MUST:

1. **Tell the user** - "No .env file found in this directory."

2. **Ask what they want to do** - Present these options:
   - **Create .env.example** - Create a template with placeholder values they can fill in
   - **Search parent directories** - Look for an existing .env in parent folders (e.g., `~/.claude/.env`)
   - **Something else** - Let them specify a custom path or approach

3. **Never silently search or create** - Even if finding a .env is easy, credentials are sensitive. Always get explicit user consent.

#### Example Interaction

```
I need database credentials but no .env file exists in this directory.

How would you like to proceed?
1. Create a .env.example template here (you'll fill in the values)
2. Search parent directories for an existing .env file
3. Something else (specify a path or approach)
```

#### When .env Exists

If `.env` exists, load it normally. Do not ask about it unless there's an error.

### Gitignore Setup (Always Do This)

**Always create a `.gitignore` file** at project setup with these entries:

```
# Credentials - NEVER commit
.env
.env.local
.env*.local

# OS files
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
.pytest_cache/

# Optional: exclude work files
work/
```

### Setup Commands
```bash
# Create project structure
mkdir -p my-analysis/{work,data}
cd my-analysis

# ALWAYS create .gitignore first
cat > .gitignore << 'EOF'
.env
.env.local
.env*.local
.DS_Store
__pycache__/
*.pyc
EOF

# Create .env.example (safe template - no real values)
cat > .env.example << 'EOF'
MYSQL_HOST=your_host_here
MYSQL_DATABASE=your_database_here
MYSQL_USER=your_user_here
MYSQL_PASSWORD=your_password_here
EOF

# Then ask user how they want to set up .env
```

### When to Promote from work/ to Root
Move a script from `work/` to the project root when:
- It answers the original question completely
- It's been tested and validated
- It's cleaned up and readable
- You're ready to share or run it regularly

---

## Phase 1: Requirements Gathering

**Before writing any code, clarify:**

1. What question is the analysis trying to answer?
2. Who will use this tool? (Data team, product, ops?)
3. How often will it run? (Ad-hoc, daily, weekly?)
4. What's the output format? (Console, CSV, HTML dashboard?)
5. Are there date range requirements?
6. Any specific filters needed? (By team, division, user type?)

## Phase 2: Data Discovery

**Explore the schema to find the right data:**

```python
# MySQL: List tables
cursor.execute("SHOW TABLES")

# MySQL: Describe a table
cursor.execute("DESCRIBE table_name")

# Redshift: List tables in schema
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'tracedb'")

# Redshift: Describe a table
cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'table_name'")
```

**Sample the data:**
```python
# See what the data looks like
cursor.execute("SELECT * FROM table_name LIMIT 10")
for row in cursor.fetchall():
    print(row)
```

**Validate assumptions:**
```python
# Check for NULLs
cursor.execute("SELECT COUNT(*) FROM table_name WHERE column IS NULL")

# Check distinct values
cursor.execute("SELECT DISTINCT column FROM table_name LIMIT 20")

# Check date ranges
cursor.execute("SELECT MIN(creation_time), MAX(creation_time) FROM table_name")
```

## Phase 3: Build the Connection Layer

**Standard structure for a CLI tool:**

```python
#!/usr/bin/env python3
"""
Tool Name
Brief description of what it does.

Usage:
    python tool_name.py [options]
"""

import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Connection function
def get_connection():
    # See mysql or redshift skill for boilerplate
    pass

# Main logic
def main():
    connection = get_connection()
    try:
        # Your analysis here
        pass
    finally:
        connection.close()

if __name__ == "__main__":
    main()
```

## Phase 4: Build Incrementally

**Start with the simplest working version:**

1. Get one data point working
2. Add date filtering
3. Add grouping/aggregation
4. Add additional filters
5. Format output
6. Add error handling
7. Add CLI arguments if needed

**Example progression:**
```python
# Step 1: Basic query
cursor.execute("SELECT COUNT(*) FROM users")

# Step 2: Add date filter
cursor.execute("SELECT COUNT(*) FROM users WHERE creation_time >= %s", (start_date,))

# Step 3: Add grouping
cursor.execute("""
    SELECT DATE(creation_time), COUNT(*)
    FROM users
    WHERE creation_time >= %s
    GROUP BY DATE(creation_time)
""", (start_date,))

# Step 4: Add more filters
cursor.execute("""
    SELECT DATE(creation_time), COUNT(*)
    FROM users
    WHERE creation_time >= %s
    AND some_column = %s
    GROUP BY DATE(creation_time)
""", (start_date, filter_value))
```

## Phase 5: Testing & Validation

**Before calling it done, use the `testing` skill for comprehensive validation.**

### Audit Artifact Checklist

Before delivery, verify:
- [ ] `audit_log.json` exists and covers all queries run
- [ ] `assumptions.md` documents business rules from ask-first interview
- [ ] `checkpoints.md` shows intermediate results match expectations
- [ ] Discoveries section lists anything learned not in skills

### Validation Checklist
1. Totals reconcile (sum of parts = whole)
2. Spot-checked 3+ known records
3. Tested with different date ranges
4. Edge cases handled (empty results, NULLs)
5. Business logic validated with user
6. **⚠️ Skill improvement offered** - Did you discover anything that should be documented?

See [testing](../testing/SKILL.md) for:
- [validation.md](../testing/validation.md) - Query result validation patterns
- [spot-checking.md](../testing/spot-checking.md) - Sample data inspection
- [checklists.md](../testing/checklists.md) - Formal pre-delivery checklists

## Phase 6: Output Formatting

**Choose the right output for your audience:**

- **Console output** - For ad-hoc analysis, quick checks
- **CSV export** - For sharing with others, import into spreadsheets
- **HTML dashboard** - For interactive exploration, sharing with non-technical users
- **JSON** - For programmatic consumption, API responses

**See `cli-patterns` for formatting utilities and `ui` for UI components and visualization patterns.**

### Required: Discoveries Section

Every analysis output MUST end with a Discoveries section:

```
## Discoveries
- [List anything learned that isn't in the skills]
- [Tables, columns, business rules, gotchas]
- If nothing new: "None - all findings were already documented"
```

This makes skill improvement a deliverable, not an afterthought.

## Common Pitfalls to Avoid

**Critical principles (see `testing` for details):**
- **NEVER SPECULATE** - Every claim must be backed by queried data
- **GET APPROVAL FOR DERIVED METRICS** - Explain methodology before building

**Query pitfalls:**
1. **Not filtering by date first** - tracked_actions is huge; date filter must come first
2. **Forgetting bidirectional relationships** - user_relationships needs UNION for both directions
3. **Ignoring NULL values** - Check what NULLs mean in each context
4. **Using SELECT * on large tables** - Always specify columns you need
5. **Not using parameterized queries** - Never concatenate strings into SQL
6. **Assuming column names are unique** - Alias columns in JOINs
7. **Not handling empty results** - Always check if query returned data
