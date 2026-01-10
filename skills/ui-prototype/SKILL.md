---
name: ui-prototype
description: >
  Create interactive HTML/CSS/JS prototypes with multi-state controls and iPhone device framing.
  Auto-triggers on: prototype, mockup, UI concept, interactive demo, wireframe, mobile UI, app screen.
  Outputs single-file HTML with hidden state controls (Cmd+Shift+P), minimal Apple-inspired design.
  Uses ui skill for design system. Asks for requirements if not provided, clarifies ambiguities,
  supports multiple concept variations (sequential or parallel via subagents), versions iterations.
---

# Trace UI Prototype

Build interactive HTML prototypes with state controls, iPhone device framing, and minimal aesthetics.

## Workflow

### 1. Gather Context

Check for existing requirements:
- Spec file referenced in conversation?
- Requirements already discussed?

If missing, ask:
```
What are you prototyping? Either:
1. Point me to a spec file
2. Describe the screens/states/interactions needed
```

### 2. Clarify Scope

Ask these questions using AskUserQuestion:

**Concept count:** "How many design concepts should I create?"
- Options: 1, 2, 3+

**Variation dimensions** (if multiple concepts): "What should differ between concepts?"
- Layout approach
- Interaction patterns
- Information density
- Let user specify

**Parallelism** (if 2+ concepts): "Build sequentially or in parallel with subagents?"

### 3. Load Design System

Invoke the `ui` skill to load design tokens and patterns. Embed the CSS variables directly in the prototype.

### 4. Build Prototype

Output requirements:
- **Single HTML file** with embedded CSS/JS
- **iPhone frame** (390×844px with notch)
- **Hidden controls** revealed via `Cmd+Shift+P` / `Ctrl+Shift+P`
- **Minimal aesthetic** - Apple meets Pinterest

Use the template structure from [assets/template.html](assets/template.html).

Reference [references/patterns.md](references/patterns.md) for:
- State control patterns
- Common interaction patterns
- Feed/list patterns
- Bottom sheet patterns

### 5. Deliver

- Save to `prototype/` folder (create if needed)
- Naming: `concept-{letter}-{descriptive-name}.html`
- Do NOT auto-open browser
- Summarize what was built and how to test controls

### 6. Iterate

On revision requests:
- Create new version: `concept-a-{name}-v2.html`
- Never overwrite existing files
- Reference previous version for context

## Controls Behavior

Hidden controls panel contains:
- Phase/mode toggles (pre-game, live, post-game, etc.)
- State switchers (empty, loading, error, success)
- Data density (empty, sparse, normal, busy)
- Custom toggles from spec

Reveal with keyboard shortcut or corner toggle button.

## Aesthetic Rules

- Generous whitespace
- Inter font family
- Subtle shadows (`box-shadow: 0 1px 3px rgb(0 0 0 / 0.1)`)
- Teal (`#18929A`) for buttons/links only
- Dark (`#393C3C`) for charts/progress
- Pill-shaped buttons (`border-radius: 9999px`)
- Smooth transitions (150-300ms)
- Touch targets min 44×44px

## File Patterns

```
prototype/
├── concept-a-{name}.html
├── concept-b-{name}.html      # if multiple
└── concept-a-{name}-v2.html   # iterations
```

## Parallel Builds

When building multiple concepts and user chooses parallel:

```
Task(subagent_type="general-purpose", prompt="Build concept A for [project]: [variation details]. Use ui skill for design system. Output to prototype/concept-a-{name}.html. Include hidden controls (Cmd+Shift+P). [Full spec context]")

Task(subagent_type="general-purpose", prompt="Build concept B for [project]: [variation details]. Use ui skill for design system. Output to prototype/concept-b-{name}.html. Include hidden controls (Cmd+Shift+P). [Full spec context]")
```

Each subagent receives:
- Full spec/requirements context
- Specific variation to explore
- Output file path
- Instruction to invoke ui skill
