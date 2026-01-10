---
name: data-analysis
description: Entry point for ALL data analysis at Trace. ALWAYS invokes ask-first skill first for requirements gathering. Use when users ask to analyze data, query databases, investigate metrics, or build reports. Routes to mysql, redshift, or stripe after requirements are clear.
---

# Data Analysis at Trace

## FIRST: Read and Follow ask-first

**STOP. Before continuing, READ [ask-first/SKILL.md](../ask-first/SKILL.md) and follow its interview process.**

Even if the request seems simple ("How many users signed up?"), the ask-first skill ensures you:
- Clarify definitions (what counts as "signed up"?)
- Confirm scope (time period, user types, exclusions)
- Validate your interpretation before running queries
- Write a project_spec.md documenting requirements

**Do not proceed with this skill until you have READ ask-first/SKILL.md, conducted its interview, and written the spec.**

---

## Quick Reference

| Data Need | Use This Skill |
|-----------|----------------|
| User/team/game lookups | mysql |
| tracked_actions (< 7 days) | mysql |
| tracked_actions (> 7 days) | redshift |
| Pre-aggregated division metrics | redshift |
| Payment/subscription data | stripe |
| CLI tool scaffolding | cli-patterns |
| HTML dashboards | ui |
| Validation before delivery | testing |

**Example prompts that trigger this skill:**
- "Analyze user signups over the last 30 days"
- "Build a dashboard showing team activity"
- "How many divisions are actively filming?"
- "Get payment data for this customer"

This skill is your entry point for building data analysis tools. It explains the data landscape, points you to the right skills, and guides you through building new tools.

## Data Landscape

Trace uses multiple data sources, each with a specific purpose:

| Source | Purpose | When to Use |
|--------|---------|-------------|
| **MySQL** | Operational database | User data, teams, games, tracked_actions, real-time queries |
| **Redshift** | Data warehouse | Large-scale analytics, pre-aggregated metrics, historical analysis |
| **Stripe** | Payment data | Subscriptions, charges, customer billing info |

## Available Skills

| Skill | Use When You Need To... |
|-------|------------------------|
| `mysql` | Query users, teams, games, tracked_actions from the operational database |
| `redshift` | Run large-scale analytics or use pre-aggregated data warehouse tables |
| `stripe` | Access payment/subscription data from Stripe |
| `cli-patterns` | Build a Python CLI tool with spinners, date parsing, data fetchers |
| `ui` | UI component library and design system for any interface |
| `testing` | Validate query results, spot-check data, run pre-delivery checks |

## Common Workflows

**"I need to analyze user activity"**
- Use `mysql` for tracked_actions queries
- Use `cli-patterns` for the CLI scaffolding

**"I need to analyze family relationships"**
- Use `mysql` for user_relationships table
- Consider BFS iteration pattern (not recursive CTEs) for performance

**"I need large-scale analytics or aggregated metrics"**
- Use `redshift` for data warehouse queries
- Note the SQL syntax differences from MySQL

**"I need payment/subscription data"**
- Use `stripe` for Stripe API access
- Use `mysql` to link Stripe customers to Trace users

**"I need to build a dashboard"**
- Use any database skill for the data layer
- Use `ui` for design principles and components
- Use `cli-patterns` if generating from CLI

## Building a New Tool: Step-by-Step

0. **Set up project structure** - Create a dedicated folder with proper organization (see [workflow.md](workflow.md) for folder structure)

1. **Requirements gathered** - By now, ask-first interview should be complete with spec written

2. **⚠️ CONFIRM YOUR INTERPRETATION** - Before writing ANY query, ask yourself: "Could this question be interpreted multiple ways?" If yes, explain your interpretation and get user approval. See [testing](../testing/SKILL.md#stop-confirm-your-approach-first) for the full checklist.

3. **Identify data sources** - Which databases/APIs have the data you need?

4. **Choose your output** - CLI report? HTML dashboard? CSV export?

5. **Set up connections** - Ensure `.env` file exists with credentials (see individual skill docs)

6. **Explore the schema** - Put exploratory scripts in `work/` subfolder

7. **Test your queries** - Validate data before building the full tool

8. **Build incrementally** - Start simple, add complexity as needed

9. **Finalize** - Move polished script to project root, clean up `work/` folder

## When to Ask the User

**Before running queries, ALWAYS confirm your interpretation when:**
- The question uses terms that aren't column names (e.g., "soccer divisions", "filming", "active")
- Multiple interpretations are possible (e.g., "both X and Y" - same entity or different?)
- Time periods are implied but not specified (e.g., "active users" - last 7 days? 30 days?)
- You need to JOIN multiple tables (confirm the relationship is correct)

**During analysis, ask when:**
- You're unsure which table contains the data needed
- Column names are ambiguous (e.g., multiple "status" columns)
- Business logic is unclear (e.g., "what counts as an active user?")
- The query returns unexpected results
- You find multiple ways to answer the question

## Key Principles

1. **Explore first, code second** - Always understand the data before writing queries
2. **Test assumptions** - Validate that columns contain what you expect
3. **Start simple** - Build the minimal working version first
4. **Use parameterized queries** - Never concatenate user input into SQL
5. **Filter by date first** - For performance on large tables like tracked_actions
6. **Clean final output** - When correcting or revising work, never include disclaimers, notes, or references to previous versions in the final output. The output should stand on its own as the intended result.

---

## 📚 Reference Files

READ these for detailed patterns:

| File | Contains | Read When... |
|------|----------|--------------|
| [workflow.md](workflow.md) | Project setup, folder structure, .env handling, 6-phase workflow, common pitfalls | Starting a new analysis project or CLI tool |
| [combining-skills.md](combining-skills.md) | Multi-source patterns, MySQL+Redshift+Stripe, data flow diagrams, dashboard generation | Combining data from multiple sources |
| [business-logic.md](business-logic.md) | Family counting algorithm, game status determination, cohort assignment, advance planner rules, FbF filtering, product type mapping | Implementing Trace-specific business rules |
| [audit-integration.md](audit-integration.md) | Query logging, checkpoint patterns, assumptions documentation | Building auditable analysis |

---

## Audit Requirements

Every analysis MUST produce these artifacts:

| Artifact | Contents | When |
|----------|----------|------|
| `audit_log.json` | All queries with params, row counts, timing | During build |
| `assumptions.md` | Business rules and definitions used | After ask-first |
| `checkpoints.md` | Intermediate results and validations | During build |

Use the patterns in [audit-integration.md](audit-integration.md).

## Continuous Skill Improvement

When you discover a gotcha, workaround, or business rule during analysis, propose adding it to the relevant skill immediately. Don't wait until the end of the project.
