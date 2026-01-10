---
name: extract-design-system
description: Extract and reverse-engineer a design system from a live web application. Use when user wants to create a design system/component library from an existing website. Requires Claude Code Chrome extension for browser automation.
---

# Extract Design System

Extract design systems from live web applications using a **template-driven subagent architecture**. The template defines completeness — subagents fill in sections until no TODOs remain.

## Core Principles

1. **Template is the contract** — The HTML template defines what "complete" looks like
2. **TODOs make incompleteness visible** — Subagents can't quit early when unfilled TODOs are obvious
3. **Sections not files** — Each subagent fills a section of ONE template, not separate files
4. **Verify what you extract** — Every value must be real computed styles, not guesses

## Prerequisites

- Claude Code Chrome extension connected
- User provides starting URL(s)
- Output location specified by user

---

## Process Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: SETUP (Main Agent)                                │
│  Copy template → Discover pages → Extract tokens → Fill CSS │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: FILL COMPONENTS (Parallel Subagents)              │
│  Each subagent: assigned section → fill ALL TODOs → return  │
│                                                             │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐  │
│  │  Subagent 1    │ │  Subagent 2    │ │  Subagent 3    │  │
│  │  Buttons       │ │  Forms         │ │  Cards/Badges  │  │
│  │  Lines 130-280 │ │  Lines 285-580 │ │  Lines 585-900 │  │
│  └────────────────┘ └────────────────┘ └────────────────┘  │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐  │
│  │  Subagent 4    │ │  Subagent 5    │ │  Subagent 6    │  │
│  │  Tables/Nav    │ │  Modals/Drops  │ │  Alerts/Progress│  │
│  │  Lines 905-1150│ │  Lines 1155-1400│ │ Lines 1405-1700│  │
│  └────────────────┘ └────────────────┘ └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: VERIFY (Main Agent)                               │
│  Check for remaining TODOs → Fix gaps → Visual verify       │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Setup (Main Agent)

### Step 1: Create Output Structure

```
{output}/
├── component-library.html    # Copy from template, will be filled
└── .extraction/
    └── screenshots/
```

Copy `component-library-template.html` to `{output}/component-library.html`.

### Step 2: Discover Pages

**If user provides URLs:** Use those.

**If no URLs provided:** Actively discover pages:
- Start at home page
- Find 4-6 distinct page types:
  - Dashboard/Home — cards, stats, widgets
  - List/Table pages — data tables, filters
  - Detail/Form pages — inputs, selects, toggles
  - Settings — toggles, checkboxes, radios
- Click "Create", "Add", "New" buttons to discover modals
- Log URLs found

### Step 3: Extract Design Tokens

Visit any page and run this JavaScript to extract CSS variables:

```javascript
// Extract all CSS custom properties
const styles = getComputedStyle(document.documentElement);
const cssVars = {};
for (const prop of document.documentElement.style) {
  if (prop.startsWith('--')) {
    cssVars[prop] = styles.getPropertyValue(prop).trim();
  }
}
// Also check stylesheets for :root variables
for (const sheet of document.styleSheets) {
  try {
    for (const rule of sheet.cssRules) {
      if (rule.selectorText === ':root') {
        for (const prop of rule.style) {
          if (prop.startsWith('--')) {
            cssVars[prop] = rule.style.getPropertyValue(prop).trim();
          }
        }
      }
    }
  } catch(e) {}
}
console.log(JSON.stringify(cssVars, null, 2));
```

### Step 4: Fill CSS Variables Section

Open `component-library.html` and fill in ALL the `:root` CSS variables (lines ~15-95).

**Replace every `/* TODO: ... */` with a real value:**

```css
/* BEFORE */
--primary: /* TODO: Extract primary brand color (hex) */;

/* AFTER */
--primary: #18929A;
```

Also fill in:
- `{{BRAND}}` in the title and h1
- `{{URL}}` in the subtitle

Save the file after filling tokens.

---

## Phase 2: Fill Components (Subagents)

### Subagent Instructions

Spawn 6 subagents in parallel. Each gets the SAME file but different sections.

**Critical instruction for ALL subagents:**

> Your job is to **replace ALL `/* TODO: ... */` comments** in your assigned section with real extracted values. Do not finish until EVERY TODO in your section is resolved. If you cannot extract a value, replace the TODO with a reasonable fallback and add a comment `/* FALLBACK - could not extract */`.

### Subagent 1: Buttons (Lines ~130-280)

```
You are filling the BUTTONS section of a design system template.

FILE: {output}/component-library.html
YOUR SECTION: Lines 130-280 (search for "SECTION 2: BUTTONS")
URLS TO VISIT: {url_list}

TASK:
1. Read the template file and find your section
2. Visit the URLs and find buttons
3. For EACH button class (.btn-primary, .btn-secondary, .btn-outline, .btn-ghost, .btn-destructive, .btn-link):
   - Extract default state styles
   - Hover the button, extract hover styles
   - Find disabled buttons, extract disabled styles
4. Extract button sizes (.btn-sm, .btn-lg)
5. Replace ALL /* TODO */ comments with real values

EXTRACTION METHOD:
Use this JavaScript to get computed styles:
```javascript
function getStyles(selector) {
  const el = document.querySelector(selector);
  if (!el) return null;
  const computed = getComputedStyle(el);
  return {
    background: computed.backgroundColor,
    color: computed.color,
    padding: computed.padding,
    borderRadius: computed.borderRadius,
    border: computed.border,
    fontSize: computed.fontSize,
    fontWeight: computed.fontWeight
  };
}
```

DO NOT FINISH until every TODO in lines 130-280 is replaced.
```

### Subagent 2: Forms (Lines ~285-580)

```
You are filling the FORMS section of a design system template.

FILE: {output}/component-library.html
YOUR SECTION: Lines 285-580 (search for "SECTION 3: FORM INPUTS" through "SECTION 4: CHECKBOXES")
URLS TO VISIT: {url_list}

TASK:
1. Read the template file and find your sections
2. Visit URLs with forms
3. Extract for EACH component:
   - .input: default, hover, focus, disabled, error states
   - .textarea: default, focus states
   - .select-trigger, .select-content, .select-item: all states
   - .checkbox: unchecked, checked, disabled states
   - .radio: unchecked, checked states
   - .toggle: off, on states
4. Click inputs to trigger focus rings - extract those styles
5. Replace ALL /* TODO */ comments with real values

DO NOT FINISH until every TODO in lines 285-580 is replaced.
```

### Subagent 3: Cards, Badges, Avatars (Lines ~585-900)

```
You are filling the CARDS, BADGES, and AVATARS sections.

FILE: {output}/component-library.html
YOUR SECTION: Lines 585-900 (search for "SECTION 5: CARDS" through "SECTION 7: AVATARS")
URLS TO VISIT: {url_list}

TASK:
1. Extract card styles (.card, .card-header, .card-content, .card-footer)
2. Extract card variants (.card-interactive hover, .card-compact, .stat-card, .card-action)
3. Extract badge variants (.badge-default through .badge-destructive)
4. Extract tag/chip styles
5. Extract avatar sizes and styles
6. Replace ALL /* TODO */ comments with real values

DO NOT FINISH until every TODO in lines 585-900 is replaced.
```

### Subagent 4: Tables & Navigation (Lines ~905-1150)

```
You are filling the TABLES and NAVIGATION sections.

FILE: {output}/component-library.html
YOUR SECTION: Lines 905-1150 (search for "SECTION 8: TABLES" and "SECTION 9: NAVIGATION")
URLS TO VISIT: {url_list}

TASK:
1. Find pages with data tables
2. Extract .table, th, td styles including hover states
3. Extract tab styles (.tabs, .tab active state)
4. Extract pill tabs (.tabs-pill, .tab-pill active state)
5. Extract filter pills (.filter-pill active state)
6. Extract breadcrumb styles
7. Replace ALL /* TODO */ comments with real values

DO NOT FINISH until every TODO in lines 905-1150 is replaced.
```

### Subagent 5: Modals & Dropdowns (Lines ~1155-1400)

```
You are filling the MODALS and DROPDOWNS sections.

FILE: {output}/component-library.html
YOUR SECTION: Lines 1155-1400 (search for "SECTION 10: MODALS" and "SECTION 11: DROPDOWNS")
URLS TO VISIT: {url_list}

TASK:
1. Click buttons that open modals (look for "Create", "Add", "Edit" buttons)
2. Extract modal styles (.modal-backdrop, .modal, .modal-header, .modal-body, .modal-footer)
3. Extract dropdown menu styles (.dropdown-content, .dropdown-item)
4. Extract tooltip styles
5. Screenshot modals open to .extraction/screenshots/modal-open.png
6. Replace ALL /* TODO */ comments with real values

DO NOT FINISH until every TODO in lines 1155-1400 is replaced.
```

### Subagent 6: Alerts, Progress, Typography (Lines ~1405-1700)

```
You are filling the ALERTS, PROGRESS, and TYPOGRAPHY sections.

FILE: {output}/component-library.html
YOUR SECTION: Lines 1405-1700 (search for "SECTION 12: ALERTS" through "SECTION 14: LINKS")
URLS TO VISIT: {url_list}

TASK:
1. Find alert/notification components
2. Extract alert variants (.alert-default, .alert-success, .alert-warning, .alert-destructive)
3. Extract progress bar styles
4. Extract skeleton loader styles if present
5. Extract link styles and hover states
6. Extract heading typography (h1-h4 sizes, weights, line-heights)
7. Replace ALL /* TODO */ comments with real values

DO NOT FINISH until every TODO in lines 1405-1700 is replaced.
```

---

## Phase 3: Verify (Main Agent)

### Step 1: Check for Remaining TODOs

Open `component-library.html` and search for `/* TODO`:

```bash
grep -c "TODO" {output}/component-library.html
```

If count > 0, identify which section and spawn a targeted subagent to fix.

### Step 2: Check for FALLBACKs

Search for `/* FALLBACK`:
- Review each one
- If the fallback looks wrong, attempt manual extraction
- If correct, leave as-is

### Step 3: Visual Verification

1. Open `component-library.html` in browser
2. Open source site in another tab
3. Compare visually:
   - Do button colors match?
   - Do input focus rings match?
   - Do card shadows match?
   - Do modal overlays match?

### Step 4: Functional Verification

Test that interactive elements work:
- Click a select dropdown — does it open?
- Click modal trigger — does modal appear?
- Click tabs — do they switch?

---

## Completion Checklist

Before declaring complete:

- [ ] `grep "TODO" component-library.html` returns 0
- [ ] All CSS variables in `:root` have real values
- [ ] All 6 subagent sections filled
- [ ] Component library opens in browser without errors
- [ ] Visual spot-check matches source site
- [ ] Interactive elements (dropdowns, modals, tabs) function

---

## Output Structure

```
{brand}-design-system/
├── component-library.html    # THE deliverable - complete design system
└── .extraction/
    └── screenshots/
        ├── modal-open.png
        └── (other reference screenshots)
```

The `component-library.html` IS the design system. No separate reference files needed.

---

---

## 📚 Reference Files

| File | Contains | Read When... |
|------|----------|--------------|
| [component-library-template.html](component-library-template.html) | HTML template with TODO placeholders for all component types, CSS variable structure | Starting extraction (copy this as output file) |
| [references/extraction-methods.md](references/extraction-methods.md) | JavaScript snippets for extracting computed styles, handling CSS-in-JS, shadow DOM traversal | Troubleshooting extraction or need specific extraction code |
| [references/output-template.md](references/output-template.md) | Expected output structure, section organization, completion criteria | Understanding what "complete" looks like |

---

## Troubleshooting

**Subagent says it's done but TODOs remain?**
- Re-run with explicit instruction: "Search for `/* TODO` in your section and fill each one"
- Specify exact line numbers

**Can't extract a style?**
- Use `getComputedStyle(element).propertyName` in browser console
- Screenshot the element for reference
- If truly impossible, use `/* FALLBACK */` with best guess

**Styles don't match source?**
- Re-extract using computed styles not inspected values
- Check for CSS-in-JS that generates unique class names
- Compare element-by-element in DevTools

**Template missing a component type?**
- Add a new section to the template following the existing pattern
- Assign to the most relevant subagent
