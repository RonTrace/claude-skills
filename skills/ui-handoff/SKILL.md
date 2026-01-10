---
name: ui-handoff
description: Extract UI components from HTML prototypes and generate a component library page. Use when user wants to: (1) create a component library from an existing HTML prototype, (2) document UI components and their states, (3) extract design tokens and reusable patterns from a prototype, (4) build a components.html reference file. Trigger phrases include "extract components", "create component library", "build components page", "document the components".
---

# Trace UI Handoff

Extract UI components from HTML prototypes and generate a standalone component library HTML page.

## Workflow

### 1. Read and Analyze the Prototype

Read the source HTML prototype file. Identify:

- **Design tokens**: CSS custom properties (colors, shadows, radii, spacing)
- **Component patterns**: Reusable UI elements (cards, buttons, badges, inputs)
- **Component states**: Variants and modifiers (active, hover, disabled, sizes)
- **Structural patterns**: Layouts, separators, containers

### 2. Categorize Components

Group components into logical sections:

| Category | Examples |
|----------|----------|
| Design Tokens | Color swatches, typography, spacing |
| Buttons & Actions | Primary, secondary, icon buttons, reaction bars |
| Cards | Content cards, media cards, status cards |
| Navigation | Tabs, breadcrumbs, phase toggles |
| Feedback | Toasts, badges, loading states |
| Layout | Separators, containers, grids |
| Form Elements | Inputs, selects, checkboxes |

### 3. Extract Each Component

For each component, capture:

```
- HTML structure (clean, standalone)
- CSS styles (only relevant rules)
- Variants/states (if any)
- Component name and description
```

### 4. Generate Component Library HTML

Create a single HTML file following the structure in [references/example-output.html](references/example-output.html).

Key sections:
1. Design tokens in `:root`
2. Library layout styles (section, grid, cards)
3. All component styles
4. Copy toast and code modal markup
5. Library header with title and description
6. Component sections with component cards
7. JavaScript for modal and copy functionality

### 5. Component Card Structure

Each component uses this card structure:

```html
<div class="component-card" data-component="[component-id]">
    <div class="component-preview">
        <!-- Live component preview -->
    </div>
    <div class="component-info">
        <div class="component-meta">
            <div class="component-name">[Component Name]</div>
            <div class="component-variant">[Variant description]</div>
        </div>
        <div class="component-actions">
            <button class="action-btn" onclick="toggleCode(this)" title="View Code">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="16 18 22 12 16 6"/>
                    <polyline points="8 6 2 12 8 18"/>
                </svg>
            </button>
            <button class="action-btn" onclick="copyCode(this)" title="Copy Code">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                </svg>
            </button>
        </div>
    </div>
    <div class="code-panel">
        <div class="code-content" data-tab="html">
            <pre><code><!-- Escaped HTML --></code></pre>
        </div>
        <div class="code-content" data-tab="css">
            <pre><code><!-- Relevant CSS --></code></pre>
        </div>
    </div>
</div>
```

## Key Patterns

### Design Token Extraction

Extract CSS custom properties from `:root` and display as color swatches:

```html
<div class="swatch-grid">
    <div class="swatch">
        <div class="swatch-color" style="background: var(--primary);"></div>
        <span class="swatch-name">--primary</span>
    </div>
</div>
```

### Component State Variants

Show multiple states in same preview when relevant:

```html
<div class="component-preview">
    <div class="flex-row">
        <button class="btn">Default</button>
        <button class="btn active">Active</button>
    </div>
</div>
```

### Code Escaping

Escape HTML entities in code panels: `<` → `&lt;`, `>` → `&gt;`, `&` → `&amp;`

### Preview Backgrounds

Use `.component-preview.dark` for light-colored components that need contrast.

## Output Naming

Name the output file based on the source:
- `prototype.html` → `prototype-components.html`
- `concept-1-cards.html` → `concept-1-cards-components.html`

## Reference

See [references/example-output.html](references/example-output.html) for a complete working example of the component library output format.
