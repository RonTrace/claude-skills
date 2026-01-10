# Data Analysis Skills Improvement - Project Update

## Date: January 10, 2025

## Problem Statement

Three issues with the data analysis skill group:

1. **Schema rediscovery** - Claude explores tables from scratch instead of using documented gotchas
2. **ask-first bypassed** - Data analysis requests skip the requirements interview
3. **No audit trail** - Analysis isn't structured for easy auditing

---

## Research Phase

### Sources Analyzed

1. **Local skills** - Read 12+ skills in this repository to understand patterns
2. **Official Anthropic skills documentation** - Best practices from claude.ai/docs
3. **Compound Engineering Plugin** (github.com/EveryInc/compound-engineering-plugin) - Multi-agent workflow patterns

### Key Findings from Research

**What makes skills effective:**
- Clear routing via rich descriptions with trigger phrases
- Progressive disclosure (SKILL.md overview → reference files for details)
- Decision tables for quick routing
- Anti-patterns documented (what NOT to do)
- Skill chaining (one skill routes to another)

**Best practice gaps in our skills:**
- Descriptions sometimes exceeded 1024 char limit
- Mixed first/third person in descriptions
- Reference files positioned as optional "Read When..." rather than required
- exploration.md taught discovery as first step, competing with table docs

---

## Implementation Phase

### Changes Made

#### Phase 1: Make ask-first Always Trigger

**[skills/data-analysis/SKILL.md](skills/data-analysis/SKILL.md)**
- Added mandatory section at top: "FIRST: Read and Follow ask-first"
- Updated description to mention ask-first requirement
- Removed old "Requirements First (Mandatory for Build Requests)" section
- Added explicit file link: `READ [ask-first/SKILL.md](../ask-first/SKILL.md)`

**[skills/ask-first/SKILL.md](skills/ask-first/SKILL.md)**
- Updated description to claim data analysis with trigger words:
  - "analyze", "query", "build", "create", "how many", "show me", "investigate", "understand", "decay", "cohort", "trend", "compare"
- Added "REQUIRED first step for: data analysis, queries, metrics, dashboards, reports, features, tools"

#### Phase 2: Reference Docs Before Exploring

**[skills/mysql/SKILL.md](skills/mysql/SKILL.md)**
- Added "Before You Query" routing table after Critical Rules
- Reframed Reference Files header as "Gotchas & Business Rules"
- Added note: "For tables not listed here, use exploration.md"

**[skills/mysql/exploration.md](skills/mysql/exploration.md)**
- Added header clarifying when to use:
  - Tables NOT documented in Reference Files
  - Discovering column values or data distributions
  - Validating assumptions about undocumented columns
- Added: "Before exploring: Check if the table has a doc in tables/"

**[skills/redshift/SKILL.md](skills/redshift/SKILL.md)** and **[skills/redshift/exploration.md](skills/redshift/exploration.md)**
- Same changes as mysql

#### Phase 3: Integrate Audit Trail

**[skills/data-analysis/SKILL.md](skills/data-analysis/SKILL.md)**
- Added Audit Requirements section with required artifacts table
- Added reference to audit-integration.md

**[skills/data-analysis/workflow.md](skills/data-analysis/workflow.md)**
- Added Audit Artifact Checklist to Phase 5

**[skills/data-analysis/audit-integration.md](skills/data-analysis/audit-integration.md)** (NEW)
- Query logging wrapper pattern (`audited_query` function)
- Assumptions documentation template
- Checkpoints pattern
- Final deliverables checklist

---

## Testing Phase

### Test 1: Initial test with subscription decay question

**Prompt:** "I want to understand the long term decay of subscriptions per division for quarterly cohorts"

**Result:**
- Claude DID ask clarifying questions using AskUserQuestion tool
- Claude did NOT read/follow the ask-first skill
- Claude just asked questions directly based on its own understanding

**Diagnosis:** "invoke ask-first" was ambiguous - Claude interpreted it as "ask some questions yourself"

### Test 2: After changing to explicit file reference

**Change made:** Updated data-analysis/SKILL.md to say "READ [ask-first/SKILL.md](../ask-first/SKILL.md) and follow its interview process"

**Result:**
- Claude tried to use a skill called "trace-data-analysis"
- Got error: "Unknown skill: trace-data-analysis"
- Then proceeded to explore data directly
- Still didn't read ask-first skill

**Diagnosis:** Plugin registration issue discovered

---

## Current Blocker: Plugin Not Registered

### Discovery

The skills at `~/.claude/skills/` are structured as a plugin (has `.claude-plugin/plugin.json`) but are NOT registered in Claude's installed plugins list.

**Evidence:**
- `~/.claude/plugins/installed_plugins.json` does not contain trace-tools
- Claude tried to invoke "trace-data-analysis" (wrong name construction)
- Skills aren't auto-loading based on descriptions

### Plugin Structure

```
~/.claude/skills/
├── .claude-plugin/
│   └── plugin.json       # Plugin metadata (name: "trace-tools")
├── skills/
│   ├── ask-first/
│   ├── data-analysis/
│   ├── mysql/
│   ├── redshift/
│   └── ...
└── README.md
```

### Options to Resolve

**Option A: Install as proper plugin**
```bash
cd ~/.claude/skills
claude plugin install .
```
This would register it in `installed_plugins.json` and make skill invocation work.

**Option B: Restructure as personal skills**
Move skills to flatter structure at `~/.claude/skills/` without the plugin wrapper.

**Option C: Debug why skills aren't auto-triggering**
Skills should auto-trigger based on description matching, not require explicit invocation. Need to understand why this isn't happening.

---

## Files Modified

| File | Status | Changes |
|------|--------|---------|
| `skills/data-analysis/SKILL.md` | Modified | ask-first gate, audit requirements |
| `skills/ask-first/SKILL.md` | Modified | Expanded description with triggers |
| `skills/mysql/SKILL.md` | Modified | Before You Query table, reframed refs |
| `skills/mysql/exploration.md` | Modified | When-to-use header |
| `skills/redshift/SKILL.md` | Modified | Same as mysql |
| `skills/redshift/exploration.md` | Modified | When-to-use header |
| `skills/data-analysis/workflow.md` | Modified | Audit checklist in Phase 5 |
| `skills/data-analysis/audit-integration.md` | Created | Query logging, checkpoints, assumptions patterns |

---

## Next Steps

1. **Resolve plugin registration** - Either install as plugin or restructure
2. **Re-test ask-first triggering** - Verify skill loads and interview runs
3. **Test schema doc usage** - Verify Claude reads table docs before exploring
4. **Test audit artifact generation** - Verify outputs include audit_log.json, assumptions.md, checkpoints.md

---

## Lessons Learned

1. **Skills don't chain via "invoke"** - Telling a skill to "invoke another skill" doesn't work reliably. Skills auto-trigger based on descriptions or need explicit file READs.

2. **Plugin structure matters** - Having `.claude-plugin/plugin.json` isn't enough; the plugin must be registered via `claude plugin install`.

3. **Description keywords are critical** - Skills trigger based on description matching user intent. More specific trigger words = better matching.

4. **Progressive disclosure works** - The "Before You Query" table pointing to reference docs is cleaner than long SKILL.md files.

5. **Audit integration should be built-in** - Making audit artifacts required (not optional) ensures accountability.
