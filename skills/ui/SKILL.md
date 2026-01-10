---
name: ui
description: Trace UI design system for all interfaces. Use when: (1) creating HTML dashboards, (2) building web apps or tools, (3) generating styled output, (4) needing component patterns. Core rules: teal (#18929A) buttons only, dark (#393C3C) charts/progress bars, pill-shaped buttons, semantic CSS variables, clean minimal design.
---

# Trace UI Design System

## CSS Variables - Copy This Exactly

```css
:root {
    /* Gray palette */
    --gray-50: #fafafa;
    --gray-100: #f4f4f5;
    --gray-200: #e4e4e7;
    --gray-300: #d4d4d8;
    --gray-400: #a1a1aa;
    --gray-500: #71717a;
    --gray-600: #52525b;
    --gray-700: #3f3f46;
    --gray-800: #27272a;
    --gray-900: #18181b;
    --gray-950: #09090b;

    /* Semantic colors - USE THESE, not raw grays */
    --background: #ffffff;
    --foreground: var(--gray-950);
    --card: #ffffff;
    --card-foreground: var(--gray-950);
    --primary: #393C3C;              /* Charts, graphs, progress bars ONLY */
    --primary-foreground: #ffffff;
    --btn-primary: #18929A;          /* Buttons and links ONLY (teal) */
    --btn-primary-hover: #147a80;
    --secondary: var(--gray-100);
    --secondary-foreground: var(--gray-900);
    --muted: var(--gray-100);
    --muted-foreground: var(--gray-500);
    --border: var(--gray-200);
    --input: var(--gray-200);
    --ring: var(--gray-950);

    /* Status colors */
    --destructive: #ef4444;
    --success: #22c55e;
    --warning: #f59e0b;

    /* Radius & Shadows */
    --radius-sm: 6px;
    --radius: 10px;
    --radius-lg: 14px;
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}
```

## Critical Rules

| Element | Correct | Wrong |
|---------|---------|-------|
| Buttons | `background: var(--btn-primary)` | `background: var(--primary)` |
| Progress bars | `background: var(--primary)` (dark) | `background: var(--btn-primary)` (teal) |
| Charts/graphs | `fill: var(--primary)` (dark) | `fill: var(--btn-primary)` (teal) |
| Button shape | `border-radius: 9999px` (pill) | Any other radius |
| Input focus | `border-color: var(--ring)` | `border-color: var(--btn-primary)` |
| Table headers | `background: var(--muted)` | `background: var(--gray-50)` |
| Muted text | `color: var(--muted-foreground)` | `color: var(--gray-500)` |
| Card radius | `border-radius: var(--radius-lg)` | `border-radius: 12px` |
| Page background | `background: var(--background)` | `background: #ffffff` |

## Anti-Patterns

```css
/* WRONG - teal is for buttons only, not charts */
.progress-bar { background: #18929A; }

/* WRONG - thick asymmetric borders */
.card { border-left: 4px solid #18929A; }

/* WRONG - teal focus ring */
input:focus { border-color: #18929A; }

/* WRONG - raw gray values instead of semantic */
.label { color: var(--gray-500); }
```

## Base Styles

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html {
    font-size: 16px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--background);
    color: var(--foreground);
    line-height: 1.5;
}
```

## Key Patterns

**Cards:**
```css
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
}
```

**Tables:**
```css
th {
    font-weight: 500;
    color: var(--muted-foreground);
    background: var(--muted);
    border-bottom: 1px solid var(--border);
}
tr:hover td { background: var(--muted); }
tr:last-child td { border-bottom: none; }
```

**Buttons:**
```css
.btn {
    background: var(--btn-primary);
    color: white;
    border: none;
    border-radius: 9999px;
    padding: 10px 16px;
    font-weight: 500;
}
.btn:hover { background: var(--btn-primary-hover); }
```

**Inputs:**
```css
.input {
    border: 1px solid var(--input);
    border-radius: var(--radius);
    background: var(--background);
    color: var(--foreground);
}
.input:focus {
    outline: none;
    border-color: var(--ring);
    box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}
```

**Progress Bars:**
```css
.progress {
    height: 8px;
    background: var(--secondary);
    border-radius: 4px;
}
.progress-bar {
    background: var(--primary);  /* Dark gray, NOT teal */
    border-radius: 4px;
}
```

---

## 📚 Reference Files

| File | Contains | Read When... |
|------|----------|--------------|
| [interactivity.md](interactivity.md) | JavaScript patterns for sorting, filtering, hover states, click handlers | Adding interactivity to dashboards or components |
| [dashboard-example.html](dashboard-example.html) | Complete working dashboard with cards, tables, charts, filters | Starting a new dashboard (copy and modify) |
| [component-library.html](component-library.html) | All components with live examples, copy-paste ready HTML/CSS | Need specific component code (buttons, inputs, cards, tables) |
