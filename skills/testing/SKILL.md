---
name: testing
description: Data validation before delivery. Use when: (1) BEFORE sharing any analysis results, (2) query results seem unexpected, (3) spot-checking data accuracy, (4) modifying existing tools. MANDATORY for stakeholder-facing output. Key rule: if you can't write the SQL in 10 seconds, the question has ambiguity - ask first.
---

# Data Validation & Testing

## Quick Reference

**The 10-Second Rule:** If you can't write the exact SQL in 10 seconds, the question has ambiguity. STOP and ask.

**Pre-Delivery Checklist:**
- [ ] Totals reconcile (sum of parts = whole)
- [ ] Spot-checked 3+ known records
- [ ] No unexpected NULLs in key columns
- [ ] JOINs didn't multiply rows (check for duplicates)
- [ ] Business logic confirmed with user

**Ambiguity Triggers (ASK FIRST if any apply):**
- Term isn't a column name ("soccer divisions", "filming", "active users")
- Time period is implied but not specified
- Combining concepts ("both X and Y")
- "Count of X" where X isn't a table name

This skill ensures your analysis is accurate before you deliver it. Use it during and after building any data analysis tool.

## STOP: Confirm Your Approach First

**Before writing ANY query, ask yourself: "Could this question be interpreted multiple ways?"**

If YES → You MUST explain your interpretation and get user approval BEFORE running queries.

### Ambiguity Triggers (If ANY apply, ASK FIRST)

| Trigger | Example |
|---------|---------|
| **Term isn't a column name** | "soccer divisions" - is that `sport_type='soccer'`? Divisions with soccer teams? |
| **Action verb is vague** | "filming" - games with video? Processed games? Any game record? |
| **Combining concepts** | "both X and Y" - same entity with both? Two separate entities? |
| **Time is implied** | "active users" - last 7 days? 30 days? Ever? |
| **"Count of X"** where X isn't a table | "families" - users? Distinct parent user_ids? Something else? |

### Example: Question With Hidden Ambiguity

**User asks:** "How many soccer divisions are filming both soccer and basketball games?"

**WRONG:** Immediately query and return a number.

**RIGHT:** Stop and ask:
```
Before I query this, I want to confirm my approach:

1. "Soccer division" - I'll look for divisions where the primary sport_type is 'soccer'.
   Or did you mean divisions that have any soccer teams?

2. "Filming" - I'll count divisions that have games with status='processed' (video delivered).
   Or should I include all scheduled games?

3. "Both soccer and basketball" - I'll find divisions where home_team games include
   BOTH sport_type='soccer' AND sport_type='basketball'.
   Is that right, or did you mean something else?

Which interpretation matches what you're looking for?
```

## Validation Mindset

**Trust but verify.** Every query result should be validated before sharing. The goal is to catch errors before stakeholders see them.

1. **Data-driven claims only** - Every number you report must be backed by a query you ran
2. **Validate incrementally** - Check results at each step, not just at the end
3. **Question unexpected results** - If something looks wrong, it probably is

## Core Principles

### NEVER SPECULATE

If you don't have data to support a claim, don't make it. Don't guess why something is happening. Query the database to find the actual reason.

If asked "why does X happen?", your answer MUST be based on actual data you've queried, not speculation. If you can't find the answer in the data, say "I don't know" and explain what you tried.

### GET APPROVAL FOR DERIVED METRICS

When measuring something requires combining multiple queries, applying filters, or using business logic rules (not just a direct `SELECT COUNT(*) FROM table WHERE column = value`), you MUST explain your methodology and get user approval BEFORE building the analysis.

**Examples that require approval:**
- "Test game" = games where `quarantine_status = 'equipment_test'` vs games where away_team matches "CMEquipmentTest"
- "Active user" = logged in last 30 days vs has a subscription vs completed an action
- "Success rate" = processed games / total games vs processed games / (processed + errors)
- "Soccer divisions filming basketball" = divisions with sport_type='soccer' that have basketball games? Or something else?

**How to ask:**
```
I'm planning to measure [METRIC]. Here's my approach:
- Definition: [how you'll identify the thing]
- Query logic: [what tables/columns you'll use]
- Filters: [what you'll include/exclude]
- Display: [how you'll show it]

Does this match your understanding, or should I adjust?
```

## When to Ask the User

**Always ask when:**

1. **Column meaning is ambiguous**
   - "I found 3 different status columns. Which one indicates active users?"
   - "Should I use `name` or `CONCAT(first_name, last_name)`?"

2. **Business logic is unclear**
   - "What counts as an 'active' user? Last login within X days?"
   - "Should coaches be included in the player count?"

3. **Data seems unexpected**
   - "I found users with NULL emails. Should these be included?"
   - "Some team_players have both is_player=1 and is_coach=1. Is this expected?"

4. **Multiple approaches possible**
   - "I can get family members via user_relationships or via shared teams. Which do you want?"
   - "Should I include historical data or only current/active records?"

5. **Results don't match expectations**
   - "The query returns 500 users but you mentioned expecting ~1000. Should I investigate?"

## Red Flags

Warning signs that something is wrong with your query or data:

- **Unexpectedly low counts** - Filter might be too restrictive
- **Unexpectedly high counts** - JOINs might be duplicating rows
- **All NULLs** - Column might be deprecated
- **Single distinct value** - Column might not be useful
- **Dates in the future** - Data quality issue
- **Negative IDs or counts** - Bug in the query

## Discovery Triggers

When these events happen, **immediately** offer to update the skills:

| When this happens... | Say this... |
|---------------------|-------------|
| You query a table not in `tables.md` | "I'm using table X which isn't documented. Want me to add it?" |
| You hit an error and find a workaround | "I discovered a gotcha: [X]. Want me to add it to the skill?" |
| The user corrects your assumption | "Thanks for the correction. Should I add this to the skill?" |
| You discover a business rule | "I learned that [X]. Should I document this?" |

These trigger **at the moment of discovery**, not at the end. Don't batch them up.

---

## 📚 Reference Files

READ these for validation patterns:

| File | Contains | Read When... |
|------|----------|--------------|
| [validation.md](validation.md) | Reconciliation patterns, NULL detection, duplicate checking, result validation | Validating query results are correct |
| [spot-checking.md](spot-checking.md) | Sample inspection techniques, known-record verification, edge case testing | Manually verifying data accuracy |
| [checklists.md](checklists.md) | Pre-delivery checklist, stakeholder review prep, sign-off procedures | Preparing to share analysis with stakeholders |
| [failures.md](failures.md) | Common failure patterns, debugging queries, fix strategies | Query returns unexpected or wrong results |

## Integration with Other Skills

Use this skill alongside:
- `mysql` / `redshift` - Validate queries against these databases
- `data-analysis` - Testing is Phase 5 of the standard workflow
- `cli-patterns` - Add validation to CLI tools before output
