# Trace Tools Plugin

A Claude Code plugin with skills for data analysis, UI design, and development workflows at Trace.

## Installation

### Prerequisites

You need git configured with SSH access to GitHub. This allows the plugin to auto-update without password prompts.

**Check if you have SSH set up:**
```bash
ssh -T git@github.com
```

If you see "Hi username! You've successfully authenticated" you're ready. If not, follow the setup below.

### Setting Up Git SSH Access

**Mac/Linux:**
```bash
# 1. Check for existing SSH key
ls ~/.ssh/id_ed25519.pub

# 2. If no key exists, create one
ssh-keygen -t ed25519 -C "your_email@trace.com"

# 3. Start SSH agent and add key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 4. Copy public key to clipboard
pbcopy < ~/.ssh/id_ed25519.pub   # Mac
# or: cat ~/.ssh/id_ed25519.pub  # Linux, then copy manually

# 5. Add to GitHub: Settings → SSH Keys → New SSH Key → Paste
```

**Windows:**
```powershell
# 1. Check for existing SSH key
dir $env:USERPROFILE\.ssh\id_ed25519.pub

# 2. If no key exists, create one
ssh-keygen -t ed25519 -C "your_email@trace.com"

# 3. Copy public key to clipboard
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard

# 4. Add to GitHub: Settings → SSH Keys → New SSH Key → Paste
```

### Install the Plugin

**Mac/Linux:**
```bash
git clone git@github.com:tracevision/trace-tools.git ~/.claude/plugins/trace-tools
```

**Windows:**
```powershell
git clone git@github.com:tracevision/trace-tools.git $env:USERPROFILE\.claude\plugins\trace-tools
```

### Auto-Updates

The plugin includes a hook that runs `git pull` every time you start Claude Code. As long as your SSH key is configured, updates happen automatically in the background.

No action needed—just start Claude Code and you'll always have the latest version.

### Environment Setup

Some skills require database credentials. Copy the template and fill in your values:

**Mac/Linux:**
```bash
cp ~/.claude/plugins/trace-tools/.env.example ~/.claude/plugins/trace-tools/.env
```

**Windows:**
```powershell
Copy-Item $env:USERPROFILE\.claude\plugins\trace-tools\.env.example $env:USERPROFILE\.claude\plugins\trace-tools\.env
```

Then edit `.env` with your credentials. Get these from your team lead or secrets manager.

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

**"Permission denied (publickey)" when cloning:**
Your SSH key isn't set up. Follow the SSH setup steps above.

**Plugin not updating:**
Check that your clone used SSH (not HTTPS):
```bash
cd ~/.claude/plugins/trace-tools
git remote -v
# Should show: git@github.com:tracevision/trace-tools.git
# If it shows https://, run:
git remote set-url origin git@github.com:tracevision/trace-tools.git
```

**Skills not appearing in Claude Code:**
Restart Claude Code. Check that the plugin is in the correct location:
```bash
ls ~/.claude/plugins/trace-tools/.claude-plugin/plugin.json
```

---

## Contributing

These skills are living documentation. When you discover a gotcha, workaround, or business rule during analysis, propose adding it to the relevant skill immediately.
