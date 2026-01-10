# Claude Skills Plugin

A Claude Code plugin with skills for data analysis, UI design, and development workflows.

## Prerequisites

**Git and GitHub access required.** This plugin uses Git for installation and auto-updates.

Ensure you have Git installed and can access GitHub repositories. If you're using SSH, verify your setup:

```bash
ssh -T git@github.com
```

If you see "Hi username! You've successfully authenticated" you're ready.

---

## Plugin Installation

### Install in Claude Code

**Mac/Linux:**
```bash
git clone https://github.com/RonTrace/claude-skills.git ~/.claude/plugins/claude-skills
```

**Windows:**
```powershell
git clone https://github.com/RonTrace/claude-skills.git $env:USERPROFILE\.claude\plugins\claude-skills
```

### Restart Claude Code

After cloning, restart Claude Code to load the plugin. The skills will appear in your skill library.

### Auto-Updates

The plugin automatically updates when you start Claude Code. No manual intervention needed.

### Environment Setup (Optional)

Some skills require database credentials. Copy the template if needed:

**Mac/Linux:**
```bash
cp ~/.claude/plugins/claude-skills/.env.example ~/.claude/plugins/claude-skills/.env
```

**Windows:**
```powershell
Copy-Item $env:USERPROFILE\.claude\plugins\claude-skills\.env.example $env:USERPROFILE\.claude\plugins\claude-skills\.env
```

Edit `.env` with your credentials (get these from your team lead or secrets manager).

---

## Quick Start

| Task | Start with |
|------|------------|
| Build/implement something | `ask-first` — gathers requirements before coding |
| Analyze data | `data-analysis` — routes to the right database |
| Create UI mockup | `ui-prototype` — interactive HTML with state controls |

---

## Available Skills

### Data Analysis

| Skill | Purpose |
|-------|---------|
| [data-analysis](skills/data-analysis/SKILL.md) | Entry point for all analysis. Routes to the right data source. |
| [mysql](skills/mysql/SKILL.md) | Query operational MySQL database for users, teams, games, tracked_actions. |
| [redshift](skills/redshift/SKILL.md) | Query Redshift data warehouse for large-scale analytics and historical data. |
| [stripe](skills/stripe/SKILL.md) | Access Stripe API for payment and subscription data. |
| [testing](skills/testing/SKILL.md) | Validate query results, spot-check data, run pre-delivery checklists. |

### UI & Design

| Skill | Purpose |
|-------|---------|
| [ui](skills/ui/SKILL.md) | Design system with CSS variables, component patterns, and styling rules. |
| [ui-prototype](skills/ui-prototype/SKILL.md) | Build interactive HTML prototypes with state controls and iPhone framing. |
| [ui-handoff](skills/ui-handoff/SKILL.md) | Extract components from prototypes into a component library. |
| [extract-design-system](skills/extract-design-system/SKILL.md) | Reverse-engineer design systems from live websites. |

### Development Tools

| Skill | Purpose |
|-------|---------|
| [ask-first](skills/ask-first/SKILL.md) | Run first for new projects. Conducts requirements interview, writes spec. |
| [cli-patterns](skills/cli-patterns/SKILL.md) | Python CLI patterns: spinners, date parsing, output formatting. |
| [common](skills/common/SKILL.md) | Shared utilities: database connections, environment loading. |

### Experimental

| Skill | Purpose |
|-------|---------|
| [nano-banana](skills/nano-banana/SKILL.md) | Python scripting and Gemini image generation. |

---

## Troubleshooting

**"Permission denied" when cloning:**
Check your GitHub access and ensure you can access the repository.

**Plugin not updating:**
Check that the clone URL is correct:
```bash
cd ~/.claude/plugins/claude-skills
git remote -v
# Should show: https://github.com/RonTrace/claude-skills.git
```

**Skills not appearing in Claude Code:**
1. Restart Claude Code
2. Verify plugin location:
```bash
ls ~/.claude/plugins/claude-skills/.claude-plugin/plugin.json
```

**Manual update (if auto-update fails):**
```bash
cd ~/.claude/plugins/claude-skills
git pull
```

---

## Contributing

These skills are living documentation. When you discover a gotcha, workaround, or business rule during analysis, propose adding it to the relevant skill immediately.
