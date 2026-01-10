# Output Template

Structure for the extracted design system skill with modular reference files.

## Directory Structure

```
{brand}-design-system/
├── SKILL.md                        # Main skill file (consolidated summary)
├── assets/
│   ├── component-library.html      # Live examples with embedded CSS
│   └── images/                     # Downloaded brand images
├── references/
│   ├── buttons.md                  # Button patterns and variants
│   ├── cards.md                    # Card patterns
│   ├── data-display.md             # Tables, stats, badges, lists
│   ├── forms.md                    # Inputs, checkboxes, toggles, selects
│   ├── icons.md                    # SVG icon library
│   ├── images.md                   # Logos, avatars, placeholders
│   ├── interactivity.md            # JS patterns (sort, filter, etc.)
│   ├── layouts.md                  # Page layouts, grids, containers
│   ├── modals.md                   # Dialogs, wizards, bottom sheets
│   └── navigation.md               # Nav, tabs, breadcrumbs, mobile menu
└── .extraction/                    # Working directory (can delete after)
    ├── discovery-checklist.md      # What's found vs extracted
    ├── source-exploration.md       # Log of URLs and discoveries
    ├── tokens.json                 # Raw extracted tokens
    └── screenshots/                # Reference screenshots (use explicit filenames!)
        ├── {page}-desktop.png      # Page screenshots at 1280px
        ├── {page}-{state}.png      # Component states (modal-open, dropdown-expanded)
        ├── mobile-nav-closed.png   # Mobile viewport (375px)
        ├── mobile-nav-open.png     # Mobile drawer open
        └── wizard-step-{n}.png     # Multi-step wizard screenshots
```

---

## SKILL.md Template

The main SKILL.md should be a **consolidated summary** with links to detailed reference files.

```markdown
---
name: {brand}-design-system
description: {Brand} UI design system for all interfaces. Use when: (1) creating HTML dashboards, (2) building web apps or tools, (3) generating styled output, (4) needing component patterns. Core rules: {primary color} buttons, {key design traits}.
---

# {Brand} Design System

## Quick Reference

| Element | Value |
|---------|-------|
| Primary Color | `{hex}` |
| Font Family | `{font}` |
| Border Radius | `{value}` |
| Primary Button | `background: var(--btn-primary)` |

## CSS Variables

Copy this block exactly:

\`\`\`css
:root {
    /* Colors */
    --primary: {value};
    --btn-primary: {value};
    --btn-primary-hover: {value};
    --background: {value};
    --foreground: {value};
    --muted: {value};
    --border: {value};

    /* Status */
    --error: {value};
    --success: {value};
    --warning: {value};

    /* Typography */
    --font-family: {value};

    /* Spacing */
    --spacing: {value};

    /* Shadows */
    --shadow-sm: {value};
    --shadow-md: {value};
    --shadow-lg: {value};

    /* Radii */
    --radius: {value};
    --radius-lg: {value};

    /* Breakpoints (reference) */
    /* --breakpoint-tablet: 768px; */
    /* --breakpoint-desktop: 1024px; */
}
\`\`\`

## Critical Rules

| Element | Correct | Wrong |
|---------|---------|-------|
| Primary buttons | `var(--btn-primary)` | `var(--primary)` |
| Charts/graphs | `var(--primary)` | `var(--btn-primary)` |
| Button shape | `border-radius: 9999px` | Square corners |

## Anti-Patterns

\`\`\`css
/* WRONG - explain why */
.button { background: blue; }

/* RIGHT */
.button { background: var(--btn-primary); }
\`\`\`

## Component Reference

Detailed patterns in reference files:

- [Buttons](references/buttons.md) - Primary, secondary, ghost, icon buttons
- [Forms](references/forms.md) - Inputs, toggles, checkboxes, selects
- [Navigation](references/navigation.md) - Desktop nav, mobile drawer, tabs
- [Cards](references/cards.md) - Standard, selectable, media cards
- [Data Display](references/data-display.md) - Tables, stats, badges
- [Modals](references/modals.md) - Dialogs, wizards, bottom sheets
- [Icons](references/icons.md) - SVG icon library
- [Layouts](references/layouts.md) - Page structure, grids
- [Interactivity](references/interactivity.md) - Sorting, filtering, hover states

## Live Examples

See [component-library.html](assets/component-library.html) for interactive examples.
```

---

## Reference File Templates

### references/buttons.md

```markdown
# Buttons

## Overview

Button styles and variants for {Brand}.

## Primary Button

**Usage:** Main actions, CTAs, form submissions

\`\`\`html
<button class="btn-primary">Label</button>
\`\`\`

\`\`\`css
.btn-primary {
    background-color: var(--btn-primary);
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 9999px;  /* pill shape */
    font-family: var(--font-family);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s;
}

.btn-primary:hover {
    background-color: var(--btn-primary-hover);
}

.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
\`\`\`

---

## Secondary Button

**Usage:** Secondary actions, cancel buttons

\`\`\`html
<button class="btn-secondary">Label</button>
\`\`\`

\`\`\`css
.btn-secondary {
    background-color: transparent;
    color: var(--foreground);
    padding: 12px 24px;
    border: 1px solid var(--border);
    border-radius: 9999px;
    /* ... */
}
\`\`\`

---

## Ghost Button

**Usage:** Tertiary actions, less prominent options

---

## Icon Button

**Usage:** Actions represented by icons (close, edit, delete)

---

## Danger Button

**Usage:** Destructive actions (delete, remove)

---

## Button States

### Hover
### Active/Pressed
### Disabled
### Loading
```

---

### references/forms.md

```markdown
# Forms

## Overview

Form inputs and controls for {Brand}.

## Text Input

### Default State

\`\`\`html
<input type="text" class="input" placeholder="Placeholder">
\`\`\`

\`\`\`css
.input {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-family: var(--font-family);
    font-size: 14px;
    background: var(--background);
    color: var(--foreground);
    transition: border-color 0.2s, box-shadow 0.2s;
}

.input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.1);
}
\`\`\`

### Error State

\`\`\`css
.input.error {
    border-color: var(--error);
}
\`\`\`

---

## Floating Label Input

{If applicable}

---

## Checkbox

---

## Radio Button

---

## Toggle Switch

---

## Select / Dropdown

---

## Textarea
```

---

### references/navigation.md

```markdown
# Navigation

## Overview

Navigation patterns for {Brand}.

## Desktop Navigation

### Primary Nav

\`\`\`html
<nav class="nav-primary">
    <a href="#" class="nav-item">Item</a>
    <a href="#" class="nav-item active">Active</a>
</nav>
\`\`\`

\`\`\`css
.nav-primary { /* ... */ }
.nav-item { /* ... */ }
.nav-item.active { /* ... */ }
\`\`\`

---

## Mobile Navigation

### Hamburger Menu Button

\`\`\`html
<button class="hamburger" aria-label="Menu">
    <!-- SVG icon -->
</button>
\`\`\`

### Mobile Drawer

\`\`\`css
.drawer {
    position: fixed;
    top: 0;
    left: 0;
    width: 280px;
    height: 100vh;
    background: var(--background);
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 1000;
}

.drawer.open {
    transform: translateX(0);
}
\`\`\`

---

## Tabs

### Underline Tabs

---

## Breadcrumbs

---

## Pagination
```

---

### references/modals.md

```markdown
# Modals & Overlays

## Overview

Modal, wizard, and overlay patterns for {Brand}.

## Standard Modal

### Structure

\`\`\`html
<div class="modal-backdrop">
    <div class="modal" role="dialog">
        <header class="modal-header">
            <h2 class="modal-title">Title</h2>
            <button class="modal-close" aria-label="Close">
                <!-- Close icon SVG -->
            </button>
        </header>
        <div class="modal-body">
            <!-- Content -->
        </div>
        <footer class="modal-footer">
            <button class="btn-secondary">Cancel</button>
            <button class="btn-primary">Confirm</button>
        </footer>
    </div>
</div>
\`\`\`

### Styles

\`\`\`css
.modal-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal {
    background: var(--background);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-lg);
    max-width: 500px;
    width: 90%;
    max-height: 90vh;
    overflow: hidden;
}

.modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
}

.modal-title {
    font-size: 18px;
    font-weight: 600;
    margin: 0;
}

.modal-close {
    /* Close button styles */
}

.modal-body {
    padding: 20px;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 16px 20px;
    border-top: 1px solid var(--border);
}
\`\`\`

---

## Multi-Step Wizard

### Header with Back Button

\`\`\`html
<header class="wizard-header">
    <button class="wizard-back">
        <!-- Back arrow SVG -->
        Back
    </button>
    <h2 class="wizard-title">Step Title</h2>
    <button class="modal-close"><!-- X --></button>
</header>
\`\`\`

### Progress Indicator

\`\`\`html
<div class="wizard-progress">
    <span class="dot active"></span>
    <span class="dot"></span>
    <span class="dot"></span>
</div>
\`\`\`

\`\`\`css
.wizard-progress {
    display: flex;
    justify-content: center;
    gap: 8px;
    padding: 12px;
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--muted);
}

.dot.active {
    background: var(--primary);
}
\`\`\`

### Continue Button Pattern

\`\`\`html
<button class="btn-primary">
    Continue
    <!-- Right arrow or > symbol -->
</button>
\`\`\`

---

## Option Cards (Selection Step)

\`\`\`html
<div class="option-card">
    <div class="option-icon"><!-- Icon --></div>
    <div class="option-content">
        <h3 class="option-title">Option Title</h3>
        <p class="option-description">Description text</p>
    </div>
</div>
\`\`\`

\`\`\`css
.option-card {
    display: flex;
    gap: 16px;
    padding: 16px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    cursor: pointer;
    transition: border-color 0.2s, background-color 0.2s;
}

.option-card:hover {
    border-color: var(--primary);
}

.option-card.selected {
    border-color: var(--primary);
    background-color: rgba(var(--primary-rgb), 0.05);
}
\`\`\`

---

## Mobile Bottom Sheet

\`\`\`css
@media (max-width: 767px) {
    .modal {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        top: auto;
        max-width: 100%;
        width: 100%;
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
        max-height: 90vh;
    }
}
\`\`\`

---

## Dropdown Menu

---

## Tooltip
```

---

### references/icons.md

```markdown
# Icons

## Overview

SVG icons extracted from {Brand}. Use inline or as components.

## Navigation Icons

### Hamburger Menu

\`\`\`html
<svg viewBox="0 0 24 24" width="24" height="24">
    <!-- path data -->
</svg>
\`\`\`

### Close / X

### Back Arrow

### Chevron (Left/Right/Up/Down)

### Home

---

## Action Icons

### Edit / Pencil

### Delete / Trash

### Add / Plus

### Search

### Copy

### Save

### Check / Checkmark

---

## Status Icons

### Success / Check Circle

### Error / X Circle

### Warning / Alert Triangle

### Info / Info Circle

---

## Media Icons

### Play

### Pause

### Volume

### Fullscreen

---

## Social Icons

{If applicable}

---

## Usage

\`\`\`css
.icon {
    width: 24px;
    height: 24px;
    fill: currentColor;
}

.icon-sm { width: 16px; height: 16px; }
.icon-lg { width: 32px; height: 32px; }
\`\`\`
```

---

### references/images.md

```markdown
# Images & Media

## Overview

Brand images, logos, placeholders, and media patterns for {Brand}.

## Logos

### Header Logo

![Header Logo](../assets/images/header-logo.{ext})

- **Dimensions:** {width}×{height}
- **Format:** {format}
- **Usage:** Site header, navigation

\`\`\`html
<a href="/" class="logo">
    <img src="/assets/images/header-logo.svg" alt="{Brand} Logo" width="{width}" height="{height}">
</a>
\`\`\`

### Footer Logo

![Footer Logo](../assets/images/footer-logo.{ext})

- **Dimensions:** {width}×{height}
- **Usage:** Site footer

### Favicon

- **16×16:** \`/favicon-16x16.png\`
- **32×32:** \`/favicon-32x32.png\`
- **Apple Touch:** \`/apple-touch-icon.png\` (180×180)

## Avatar Defaults

### Default User Avatar

![Default Avatar](../assets/images/default-avatar.{ext})

- **Dimensions:** {width}×{height}
- **Shape:** {circle|rounded|square}
- **Border Radius:** \`{value}\`

\`\`\`css
.avatar {
    width: {size}px;
    height: {size}px;
    border-radius: {50%|var(--radius)};
    object-fit: cover;
}

.avatar-sm { width: 32px; height: 32px; }
.avatar-md { width: 48px; height: 48px; }
.avatar-lg { width: 64px; height: 64px; }
\`\`\`

## Empty States

### No Data Illustration

![Empty State](../assets/images/empty-state.{ext})

- **Dimensions:** {width}×{height}
- **Usage:** Empty tables, no search results, blank dashboards

## Background Patterns

### Hero Background

\`\`\`css
.hero {
    background-image: url('/assets/images/hero-bg.{ext}');
    background-size: {cover|contain|{value}};
    background-position: {center|top|{value}};
    background-repeat: {no-repeat|repeat};
}
\`\`\`

## Image URLs Reference

Downloaded images saved to \`assets/images/\`:

| Type | Filename | Source URL |
|------|----------|------------|
| Header Logo | header-logo.svg | {url} |
| Footer Logo | footer-logo.svg | {url} |
| Favicon | favicon.ico | {url} |
| Default Avatar | default-avatar.png | {url} |
| Empty State | empty-state.svg | {url} |
```

---

### references/data-display.md

```markdown
# Data Display

## Overview

Tables, stats, badges, and list patterns for {Brand}.

## Tables

### Basic Table

\`\`\`html
<table class="table">
    <thead>
        <tr>
            <th>Column</th>
            <th>Column</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Data</td>
            <td>Data</td>
        </tr>
    </tbody>
</table>
\`\`\`

\`\`\`css
.table {
    width: 100%;
    border-collapse: collapse;
}

.table th {
    text-align: left;
    padding: 12px 16px;
    font-weight: 600;
    color: var(--muted-foreground);
    border-bottom: 1px solid var(--border);
}

.table td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--border);
}

.table tbody tr:hover {
    background-color: var(--muted);
}
\`\`\`

### Sortable Headers

\`\`\`css
.table th.sortable {
    cursor: pointer;
}

.table th.sort-asc::after {
    content: ' ↑';
}

.table th.sort-desc::after {
    content: ' ↓';
}
\`\`\`

### Responsive Table (Mobile)

\`\`\`css
@media (max-width: 767px) {
    .table-responsive table,
    .table-responsive thead,
    .table-responsive tbody,
    .table-responsive tr,
    .table-responsive th,
    .table-responsive td {
        display: block;
    }

    .table-responsive thead {
        display: none;
    }

    .table-responsive tr {
        margin-bottom: 16px;
        border: 1px solid var(--border);
        border-radius: var(--radius);
    }

    .table-responsive td {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid var(--border);
    }

    .table-responsive td::before {
        content: attr(data-label);
        font-weight: 600;
    }
}
\`\`\`

---

## Stats Card

\`\`\`html
<div class="stat-card">
    <div class="stat-value">1,234</div>
    <div class="stat-label">Total Users</div>
</div>
\`\`\`

---

## Badge / Tag

\`\`\`html
<span class="badge">Label</span>
<span class="badge badge-success">Active</span>
<span class="badge badge-error">Inactive</span>
\`\`\`

---

## List Items

---

## Empty State

\`\`\`html
<div class="empty-state">
    <div class="empty-icon"><!-- Icon --></div>
    <h3 class="empty-title">No items found</h3>
    <p class="empty-description">Description or call to action</p>
    <button class="btn-primary">Add Item</button>
</div>
\`\`\`
```

---

### references/cards.md

```markdown
# Cards

## Overview

Card patterns for {Brand}.

## Standard Card

\`\`\`html
<div class="card">
    <div class="card-body">
        <h3 class="card-title">Title</h3>
        <p class="card-text">Content</p>
    </div>
</div>
\`\`\`

\`\`\`css
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    overflow: hidden;
}

.card-body {
    padding: 20px;
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
}
\`\`\`

---

## Media Card

With image or video thumbnail.

---

## Selectable Option Card

See [modals.md](modals.md#option-cards-selection-step) for wizard selection cards.

---

## Dashed "Create New" Card

\`\`\`html
<button class="card-create">
    <span class="card-create-icon">+</span>
    <span class="card-create-text">Add New Item</span>
</button>
\`\`\`

\`\`\`css
.card-create {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 32px;
    border: 2px dashed var(--border);
    border-radius: var(--radius-lg);
    background: transparent;
    color: var(--muted-foreground);
    cursor: pointer;
    transition: border-color 0.2s, color 0.2s;
}

.card-create:hover {
    border-color: var(--primary);
    color: var(--primary);
}
\`\`\`
```

---

### references/layouts.md

```markdown
# Layouts

## Overview

Page layout patterns for {Brand}.

## Container

\`\`\`css
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}
\`\`\`

---

## Grid System

\`\`\`css
.grid {
    display: grid;
    gap: 20px;
}

.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }

@media (max-width: 767px) {
    .grid-2, .grid-3, .grid-4 {
        grid-template-columns: 1fr;
    }
}
\`\`\`

---

## Page Header

---

## Page Footer

---

## Sidebar Layout

---

## Responsive Breakpoints

| Breakpoint | Width | Usage |
|------------|-------|-------|
| Mobile | < 768px | Single column |
| Tablet | 768px - 1023px | 2 columns |
| Desktop | ≥ 1024px | Full layout |
```

---

### references/interactivity.md

```markdown
# Interactivity

## Overview

JavaScript patterns for sorting, filtering, and user interaction.

## Filtering

### Toggle Group

\`\`\`html
<div class="toggle-group">
    <button class="toggle active">All</button>
    <button class="toggle">Option A</button>
    <button class="toggle">Option B</button>
</div>
\`\`\`

\`\`\`css
.toggle-group {
    display: inline-flex;
    border: 1px solid var(--border);
    border-radius: 9999px;
    overflow: hidden;
}

.toggle {
    padding: 8px 16px;
    background: transparent;
    border: none;
    cursor: pointer;
}

.toggle.active {
    background: var(--primary);
    color: white;
}
\`\`\`

---

## Sorting

### Sortable Table JavaScript

\`\`\`javascript
function sortTable(table, column, ascending = true) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
        const aVal = a.cells[column].textContent.trim();
        const bVal = b.cells[column].textContent.trim();
        return ascending
            ? aVal.localeCompare(bVal, undefined, { numeric: true })
            : bVal.localeCompare(aVal, undefined, { numeric: true });
    });

    rows.forEach(row => tbody.appendChild(row));
}
\`\`\`

---

## Hover Effects

### Row Highlighting

\`\`\`css
tbody tr {
    transition: background-color 0.15s;
}

tbody tr:hover {
    background-color: var(--muted);
}
\`\`\`

---

## Loading States

### Spinner

\`\`\`html
<div class="spinner"></div>
\`\`\`

\`\`\`css
.spinner {
    width: 24px;
    height: 24px;
    border: 2px solid var(--muted);
    border-top-color: var(--primary);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
\`\`\`

### Skeleton Loader

---

## Tooltips

---

## Collapsible Sections
```

---

## assets/component-library.html Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Brand} Component Library</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family={Font}:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* === CSS VARIABLES === */
        :root {
            /* Paste extracted variables here */
        }

        /* === BASE STYLES === */
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: var(--font-family), sans-serif;
            background: var(--background);
            color: var(--foreground);
            line-height: 1.5;
        }

        /* === COMPONENT STYLES === */
        /* Paste component CSS here */

        /* === DEMO LAYOUT === */
        .demo-container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .demo-section { margin-bottom: 3rem; }
        .demo-section h2 {
            margin-bottom: 1rem;
            font-size: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border);
        }
        .demo-grid { display: flex; flex-wrap: wrap; gap: 1rem; align-items: flex-start; }
        .demo-note { color: var(--muted-foreground); font-size: 0.875rem; margin-bottom: 1rem; }

        /* Viewport indicator */
        .viewport-indicator {
            position: fixed;
            bottom: 1rem;
            right: 1rem;
            padding: 0.5rem 1rem;
            background: var(--foreground);
            color: var(--background);
            border-radius: var(--radius);
            font-size: 0.75rem;
            font-family: monospace;
            z-index: 9999;
        }
    </style>
</head>
<body>
    <div class="demo-container">
        <h1>{Brand} Component Library</h1>
        <p class="demo-note">Resize browser to test responsive behavior</p>

        <!-- Colors -->
        <section class="demo-section">
            <h2>Colors</h2>
            <div class="demo-grid">
                <!-- Color swatches -->
            </div>
        </section>

        <!-- Typography -->
        <section class="demo-section">
            <h2>Typography</h2>
            <!-- Headings, body text -->
        </section>

        <!-- Buttons -->
        <section class="demo-section">
            <h2>Buttons</h2>
            <div class="demo-grid">
                <!-- Button variants -->
            </div>
        </section>

        <!-- Forms -->
        <section class="demo-section">
            <h2>Form Inputs</h2>
            <!-- Input examples -->
        </section>

        <!-- Cards -->
        <section class="demo-section">
            <h2>Cards</h2>
            <div class="demo-grid">
                <!-- Card examples -->
            </div>
        </section>

        <!-- Tables -->
        <section class="demo-section">
            <h2>Tables</h2>
            <!-- Table example -->
        </section>

        <!-- Modals -->
        <section class="demo-section">
            <h2>Modals</h2>
            <button class="btn-primary" onclick="document.getElementById('demo-modal').style.display='flex'">
                Open Modal
            </button>
            <!-- Modal HTML -->
        </section>

        <!-- Navigation -->
        <section class="demo-section">
            <h2>Navigation</h2>
            <!-- Nav examples -->
        </section>

        <!-- Icons -->
        <section class="demo-section">
            <h2>Icons</h2>
            <div class="demo-grid">
                <!-- SVG icons -->
            </div>
        </section>
    </div>

    <!-- Viewport Indicator -->
    <div class="viewport-indicator" id="viewport"></div>

    <script>
    // Viewport indicator
    function updateViewport() {
        const w = window.innerWidth;
        const label = w < 768 ? 'Mobile' : w < 1024 ? 'Tablet' : 'Desktop';
        document.getElementById('viewport').textContent = `${w}px (${label})`;
    }
    window.addEventListener('resize', updateViewport);
    updateViewport();

    // Modal close
    document.querySelectorAll('.modal-close, .modal-backdrop').forEach(el => {
        el.addEventListener('click', (e) => {
            if (e.target === el) {
                el.closest('.modal-backdrop')?.style.display = 'none';
            }
        });
    });
    </script>
</body>
</html>
```

---

## Extraction Checklist

Before finalizing, verify completion:

### Design Tokens
- [ ] CSS custom properties from :root
- [ ] Color palette complete
- [ ] Typography scale documented
- [ ] Spacing values
- [ ] Border radii
- [ ] Shadows

### Components (Reference Files)
- [ ] buttons.md - All variants and states
- [ ] forms.md - All input types
- [ ] navigation.md - Desktop + mobile patterns
- [ ] cards.md - All variants
- [ ] data-display.md - Tables, stats, badges
- [ ] modals.md - Standard + wizard patterns
- [ ] icons.md - Comprehensive SVG library
- [ ] layouts.md - Grid, containers, page patterns
- [ ] interactivity.md - JS patterns

### Responsive
- [ ] Mobile navigation (hamburger, drawer)
- [ ] Mobile modal (bottom sheet)
- [ ] Mobile table (stacked)
- [ ] Touch targets ≥ 44px

### Quality
- [ ] component-library.html renders correctly
- [ ] Tested at 375px, 768px, 1280px
- [ ] Source exploration log complete
