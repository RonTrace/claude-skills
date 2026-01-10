# Extraction Methods

JavaScript snippets organized by **subagent domain**. Each section is self-contained — copy only the section your subagent needs.

---

## Utilities (Include in all subagents)

```javascript
// RGB to Hex converter
function rgbToHex(rgb) {
  const match = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!match) return rgb;
  return '#' + [match[1], match[2], match[3]]
    .map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
}

// Extract computed styles for any element
function getStyles(el) {
  if (!el) return null;
  const s = getComputedStyle(el);
  return {
    // Box
    width: s.width, height: s.height,
    padding: s.padding, margin: s.margin,
    border: s.border, borderRadius: s.borderRadius,
    // Colors
    background: s.backgroundColor, color: s.color, borderColor: s.borderColor,
    // Typography
    fontFamily: s.fontFamily, fontSize: s.fontSize,
    fontWeight: s.fontWeight, lineHeight: s.lineHeight,
    letterSpacing: s.letterSpacing, textTransform: s.textTransform,
    // Effects
    boxShadow: s.boxShadow, opacity: s.opacity,
    // Layout
    display: s.display, gap: s.gap,
    // Misc
    cursor: s.cursor, transition: s.transition
  };
}

// Compare two style objects, return differences
function diffStyles(before, after) {
  const diff = {};
  for (const [k, v] of Object.entries(after)) {
    if (before[k] !== v) diff[k] = { from: before[k], to: v };
  }
  return diff;
}
```

---

## 1. extract-tokens

**Output:** `.extraction/tokens.json`

### CSS Custom Properties

```javascript
const cssVars = {};
for (const sheet of document.styleSheets) {
  try {
    for (const rule of sheet.cssRules) {
      if (rule.selectorText === ':root') {
        const matches = rule.cssText.matchAll(/--([^:]+):\s*([^;]+)/g);
        for (const m of matches) cssVars[`--${m[1].trim()}`] = m[2].trim();
      }
    }
  } catch (e) { /* cross-origin */ }
}
cssVars;
```

### Colors (from computed styles)

```javascript
const colors = { backgrounds: new Set(), text: new Set(), borders: new Set() };
document.querySelectorAll('*').forEach(el => {
  const s = getComputedStyle(el);
  if (s.backgroundColor !== 'rgba(0, 0, 0, 0)') colors.backgrounds.add(s.backgroundColor);
  if (s.color) colors.text.add(s.color);
  if (s.borderColor !== 'rgb(0, 0, 0)') colors.borders.add(s.borderColor);
});
({
  backgrounds: [...colors.backgrounds].map(c => ({ rgb: c, hex: rgbToHex(c) })),
  text: [...colors.text].map(c => ({ rgb: c, hex: rgbToHex(c) })),
  borders: [...colors.borders].map(c => ({ rgb: c, hex: rgbToHex(c) }))
});
```

### Typography Scale

```javascript
const fonts = new Set();
const sizes = new Map();
document.querySelectorAll('*').forEach(el => {
  const s = getComputedStyle(el);
  fonts.add(s.fontFamily);
  const size = s.fontSize;
  if (!sizes.has(size)) sizes.set(size, []);
  if (!sizes.get(size).includes(el.tagName)) sizes.get(size).push(el.tagName);
});
({
  fontFamilies: [...fonts],
  fontSizes: [...sizes.entries()]
    .sort((a, b) => parseFloat(a[0]) - parseFloat(b[0]))
    .map(([size, tags]) => ({ size, usedIn: tags.slice(0, 3) }))
});
```

### Heading Styles

```javascript
['h1','h2','h3','h4','h5','h6'].map(tag => {
  const el = document.querySelector(tag);
  if (!el) return { tag, found: false };
  const s = getComputedStyle(el);
  return { tag, fontSize: s.fontSize, fontWeight: s.fontWeight, lineHeight: s.lineHeight, letterSpacing: s.letterSpacing };
});
```

### Spacing & Radii

```javascript
const spacing = new Set(), radii = new Set();
document.querySelectorAll('*').forEach(el => {
  const s = getComputedStyle(el);
  ['padding','margin','gap'].forEach(p => {
    if (s[p] && s[p] !== '0px') s[p].split(' ').forEach(v => spacing.add(v));
  });
  if (s.borderRadius && s.borderRadius !== '0px') radii.add(s.borderRadius);
});
({
  spacing: [...spacing].filter(v => v.endsWith('px')).sort((a,b) => parseFloat(a)-parseFloat(b)),
  radii: [...radii].sort((a,b) => parseFloat(a)-parseFloat(b))
});
```

### Shadows

```javascript
const shadows = new Set();
document.querySelectorAll('*').forEach(el => {
  const shadow = getComputedStyle(el).boxShadow;
  if (shadow && shadow !== 'none') shadows.add(shadow);
});
[...shadows];
```

---

## 2. extract-buttons

**Output:** `references/buttons.md`

### Find All Buttons

```javascript
const buttons = [];
document.querySelectorAll('button, [role="button"], a.btn, [class*="btn"]').forEach(btn => {
  buttons.push({
    text: btn.textContent?.trim().substring(0, 30),
    className: btn.className,
    styles: getStyles(btn),
    hasIcon: !!btn.querySelector('svg'),
    isDisabled: btn.disabled || btn.classList.contains('disabled')
  });
});
buttons;
```

### Extract Button with States

```javascript
function extractButtonWithStates(selector) {
  const btn = document.querySelector(selector);
  if (!btn) return null;

  // Default state
  const defaultState = getStyles(btn);

  // Hover state (try adding class)
  btn.classList.add('hover');
  const hoverState = getStyles(btn);
  btn.classList.remove('hover');

  // Disabled state (find a disabled button or simulate)
  const disabledBtn = document.querySelector(`${selector}:disabled, ${selector}.disabled`);
  const disabledState = disabledBtn ? getStyles(disabledBtn) : null;

  return {
    selector,
    default: defaultState,
    hover: diffStyles(defaultState, hoverState),
    disabled: disabledState
  };
}
extractButtonWithStates('.btn-primary');
```

### Categorize Button Variants

```javascript
const variants = { primary: [], secondary: [], ghost: [], icon: [], danger: [] };
document.querySelectorAll('button, [role="button"]').forEach(btn => {
  const cls = btn.className.toLowerCase();
  const data = { text: btn.textContent?.trim(), styles: getStyles(btn) };
  if (cls.includes('primary') || cls.includes('cta')) variants.primary.push(data);
  else if (cls.includes('secondary') || cls.includes('outline')) variants.secondary.push(data);
  else if (cls.includes('ghost') || cls.includes('text')) variants.ghost.push(data);
  else if (cls.includes('icon') || (!btn.textContent?.trim() && btn.querySelector('svg'))) variants.icon.push(data);
  else if (cls.includes('danger') || cls.includes('destructive')) variants.danger.push(data);
});
variants;
```

---

## 3. extract-forms

**Output:** `references/forms.md`

### Text Input with States

```javascript
function extractInputWithStates(selector) {
  const input = document.querySelector(selector);
  if (!input) return null;

  // Default
  const defaultState = getStyles(input);

  // Focus (trigger it)
  input.focus();
  const focusState = getStyles(input);
  input.blur();

  // Error (find one or check class)
  const errorInput = document.querySelector(`${selector}.error, ${selector}[aria-invalid="true"]`);
  const errorState = errorInput ? getStyles(errorInput) : null;

  // Disabled
  const disabledInput = document.querySelector(`${selector}:disabled`);
  const disabledState = disabledInput ? getStyles(disabledInput) : null;

  return {
    default: defaultState,
    focus: diffStyles(defaultState, focusState),
    error: errorState,
    disabled: disabledState
  };
}
extractInputWithStates('input[type="text"]');
```

### Select/Dropdown

```javascript
function extractSelect(selector) {
  const select = document.querySelector(selector);
  if (!select) return null;

  const closed = getStyles(select);

  // Try to find open state (custom dropdowns)
  const openDropdown = document.querySelector('[class*="dropdown"][class*="open"], [class*="select"][class*="open"]');
  const openState = openDropdown ? getStyles(openDropdown) : null;

  // Options
  const options = select.querySelectorAll('option');
  const optionStyles = options[0] ? getStyles(options[0]) : null;

  return { closed, open: openState, optionStyles, optionCount: options.length };
}
extractSelect('select');
```

### Checkbox & Toggle

```javascript
function extractCheckbox() {
  const unchecked = document.querySelector('input[type="checkbox"]:not(:checked)');
  const checked = document.querySelector('input[type="checkbox"]:checked');

  return {
    unchecked: unchecked ? getStyles(unchecked) : null,
    checked: checked ? getStyles(checked) : null,
    // Custom checkbox (label-based)
    customUnchecked: unchecked?.nextElementSibling ? getStyles(unchecked.nextElementSibling) : null,
    customChecked: checked?.nextElementSibling ? getStyles(checked.nextElementSibling) : null
  };
}
extractCheckbox();
```

### Toggle Switch

```javascript
const toggle = document.querySelector('[class*="toggle"], [class*="switch"]');
if (toggle) {
  const input = toggle.querySelector('input') || toggle;
  const isOn = input.checked || toggle.classList.contains('on') || toggle.classList.contains('active');
  ({
    element: toggle.outerHTML.substring(0, 500),
    isOn,
    styles: getStyles(toggle),
    trackStyles: getStyles(toggle.querySelector('[class*="track"]')),
    thumbStyles: getStyles(toggle.querySelector('[class*="thumb"], [class*="knob"]'))
  });
}
```

---

## 4. extract-navigation

**Output:** `references/navigation.md`

### Desktop Nav

```javascript
const nav = document.querySelector('nav, header nav, [role="navigation"]');
if (nav) ({
  styles: getStyles(nav),
  items: [...nav.querySelectorAll('a, button')].slice(0, 10).map(item => ({
    text: item.textContent?.trim(),
    styles: getStyles(item),
    isActive: item.classList.contains('active') || item.getAttribute('aria-current')
  }))
});
```

### Tabs

```javascript
const tabContainer = document.querySelector('[role="tablist"], [class*="tabs"]');
if (tabContainer) {
  const tabs = tabContainer.querySelectorAll('[role="tab"], [class*="tab"]');
  const activeTab = tabContainer.querySelector('[aria-selected="true"], .active, [class*="active"]');
  ({
    container: getStyles(tabContainer),
    tab: tabs[0] ? getStyles(tabs[0]) : null,
    activeTab: activeTab ? getStyles(activeTab) : null,
    indicatorStyles: getStyles(tabContainer.querySelector('[class*="indicator"]'))
  });
}
```

### Mobile Hamburger (run at 375px viewport)

```javascript
const hamburger = document.querySelector(
  '[class*="hamburger" i], [class*="menu-toggle" i], [aria-label*="menu" i]'
);
if (hamburger) ({
  html: hamburger.outerHTML,
  styles: getStyles(hamburger),
  icon: hamburger.querySelector('svg')?.outerHTML
});
```

### Mobile Drawer (click hamburger first)

```javascript
const drawer = document.querySelector(
  '[class*="drawer" i], [class*="mobile-nav" i], [class*="sidebar" i]:not([class*="desktop"])'
);
if (drawer) {
  const s = getComputedStyle(drawer);
  ({
    styles: getStyles(drawer),
    position: { left: s.left, right: s.right, width: s.width },
    navItems: [...drawer.querySelectorAll('a, button')].slice(0, 10).map(item => ({
      text: item.textContent?.trim(),
      styles: getStyles(item)
    })),
    closeButton: drawer.querySelector('[class*="close"], [aria-label*="close"]')?.outerHTML
  });
}
```

### Breadcrumbs

```javascript
const breadcrumb = document.querySelector('[class*="breadcrumb"], [aria-label="breadcrumb"]');
if (breadcrumb) ({
  container: getStyles(breadcrumb),
  items: [...breadcrumb.querySelectorAll('a, span')].map(item => ({
    text: item.textContent?.trim(),
    styles: getStyles(item)
  })),
  separator: breadcrumb.querySelector('[class*="separator"], [class*="divider"]')?.textContent
});
```

---

## 5. extract-cards

**Output:** `references/cards.md`

### Find All Card Variants

```javascript
const cards = [];
document.querySelectorAll('[class*="card"]').forEach(card => {
  const cls = card.className.toLowerCase();
  cards.push({
    type: cls.includes('dashed') ? 'create' : cls.includes('stat') ? 'stat' : 'standard',
    styles: getStyles(card),
    hasImage: !!card.querySelector('img, video'),
    hasTitle: !!card.querySelector('h1,h2,h3,h4,h5,h6,[class*="title"]'),
    html: card.outerHTML.substring(0, 500)
  });
});
cards.slice(0, 10);
```

### Card Internal Structure

```javascript
function extractCardStructure(selector) {
  const card = document.querySelector(selector);
  if (!card) return null;
  return {
    container: getStyles(card),
    header: getStyles(card.querySelector('[class*="header"]')),
    body: getStyles(card.querySelector('[class*="body"], [class*="content"]')),
    footer: getStyles(card.querySelector('[class*="footer"], [class*="actions"]')),
    title: getStyles(card.querySelector('[class*="title"], h1, h2, h3')),
    image: getStyles(card.querySelector('img'))
  };
}
extractCardStructure('.card');
```

### Dashed "Create" Card

```javascript
const createCard = document.querySelector('[class*="dashed"], [class*="create"], [class*="add-new"]');
if (createCard) ({
  styles: getStyles(createCard),
  icon: createCard.querySelector('svg, [class*="icon"], [class*="plus"]')?.outerHTML,
  text: createCard.textContent?.trim()
});
```

---

## 6. extract-data-display

**Output:** `references/data-display.md`

### Table

```javascript
const table = document.querySelector('table');
if (table) {
  const th = table.querySelector('th');
  const td = table.querySelector('td');
  const row = table.querySelector('tbody tr');
  ({
    table: getStyles(table),
    header: getStyles(th),
    cell: getStyles(td),
    row: getStyles(row),
    columns: [...table.querySelectorAll('th')].map(h => h.textContent?.trim()),
    hasSorting: !!table.querySelector('[class*="sort"]'),
    hasCheckbox: !!table.querySelector('input[type="checkbox"]')
  });
}
```

### Avatar/Initials

```javascript
const avatar = document.querySelector('[class*="avatar"], [class*="initials"]');
if (avatar) ({
  styles: getStyles(avatar),
  isCircular: getComputedStyle(avatar).borderRadius === '50%',
  size: { width: getComputedStyle(avatar).width, height: getComputedStyle(avatar).height },
  text: avatar.textContent?.trim()
});
```

### Badges & Tags

```javascript
const badges = [];
document.querySelectorAll('[class*="badge"], [class*="tag"], [class*="chip"], [class*="pill"]').forEach(badge => {
  badges.push({
    text: badge.textContent?.trim(),
    styles: getStyles(badge),
    variant: badge.className
  });
});
badges.slice(0, 10);
```

### Empty State

```javascript
const empty = document.querySelector('[class*="empty"], [class*="no-data"], [class*="no-results"]');
if (empty) ({
  styles: getStyles(empty),
  icon: empty.querySelector('svg, img')?.outerHTML?.substring(0, 500),
  title: empty.querySelector('h1,h2,h3,[class*="title"]')?.textContent,
  description: empty.querySelector('p,[class*="description"]')?.textContent,
  action: empty.querySelector('button, a')?.outerHTML
});
```

---

## 7. extract-modals

**Output:** `references/modals.md`

### Modal Structure (trigger modal first)

```javascript
const modal = document.querySelector('[role="dialog"], [class*="modal"], [class*="dialog"]');
if (modal) {
  const s = getComputedStyle(modal);
  ({
    container: {
      width: s.width, maxWidth: s.maxWidth,
      padding: s.padding, borderRadius: s.borderRadius,
      boxShadow: s.boxShadow, background: s.backgroundColor
    },
    header: getStyles(modal.querySelector('[class*="header"]')),
    title: getStyles(modal.querySelector('[class*="title"], h1, h2')),
    closeButton: {
      html: modal.querySelector('[class*="close"], [aria-label*="close"]')?.outerHTML,
      styles: getStyles(modal.querySelector('[class*="close"]'))
    },
    body: getStyles(modal.querySelector('[class*="body"], [class*="content"]')),
    footer: getStyles(modal.querySelector('[class*="footer"], [class*="actions"]')),
    footerButtons: [...(modal.querySelector('[class*="footer"]')?.querySelectorAll('button') || [])].map(b => ({
      text: b.textContent?.trim(),
      styles: getStyles(b)
    }))
  });
}
```

### Backdrop

```javascript
const backdrop = document.querySelector('[class*="backdrop"], [class*="overlay"]');
if (backdrop) getStyles(backdrop);
```

### Wizard Progress Indicator

```javascript
const progress = document.querySelector('[class*="progress"], [class*="steps"], [class*="indicator"]');
if (progress) {
  const dots = progress.querySelectorAll('[class*="dot"], [class*="step"], li');
  const active = progress.querySelector('[class*="active"], [class*="current"]');
  ({
    container: getStyles(progress),
    totalSteps: dots.length,
    dot: dots[0] ? getStyles(dots[0]) : null,
    activeDot: active ? getStyles(active) : null
  });
}
```

### Wizard Navigation Buttons

```javascript
const backBtn = document.querySelector('[class*="back"]:not([class*="background"])')
  || [...document.querySelectorAll('button')].find(b => b.textContent?.trim().toLowerCase() === 'back');
const nextBtn = document.querySelector('[class*="continue"], [class*="next"]')
  || [...document.querySelectorAll('button')].find(b => /continue|next/i.test(b.textContent));
({
  back: backBtn ? { html: backBtn.outerHTML, styles: getStyles(backBtn) } : null,
  next: nextBtn ? { html: nextBtn.outerHTML, styles: getStyles(nextBtn) } : null
});
```

### Option Cards (wizard selection)

```javascript
const options = document.querySelectorAll('[class*="option"], [class*="choice"], [role="radio"]');
if (options.length) {
  const selected = [...options].find(o => o.classList.contains('selected') || o.querySelector(':checked'));
  ({
    count: options.length,
    default: getStyles(options[0]),
    selected: selected ? getStyles(selected) : 'Click one to see selected state',
    html: options[0]?.outerHTML?.substring(0, 500)
  });
}
```

---

## 8. extract-icons

**Output:** `references/icons.md`

### Extract All Unique SVGs

```javascript
const svgMap = new Map();
document.querySelectorAll('svg').forEach(svg => {
  const paths = [...svg.querySelectorAll('path')].map(p => p.getAttribute('d')).filter(Boolean).join('|');
  const key = paths || svg.innerHTML.trim();
  if (key && !svgMap.has(key)) {
    const parent = svg.closest('button, a, [role="button"]');
    svgMap.set(key, {
      svg: svg.outerHTML,
      viewBox: svg.getAttribute('viewBox'),
      size: { width: svg.getAttribute('width') || getComputedStyle(svg).width, height: svg.getAttribute('height') || getComputedStyle(svg).height },
      name: svg.getAttribute('aria-label') || parent?.getAttribute('aria-label') || svg.className?.baseVal || 'unknown',
      context: parent?.tagName || svg.parentElement?.tagName
    });
  }
});
({ total: svgMap.size, icons: [...svgMap.values()] });
```

### Categorize Icons

```javascript
const icons = [...svgMap.values()];
const cats = { nav: [], action: [], status: [], media: [], other: [] };
icons.forEach(icon => {
  const n = icon.name.toLowerCase();
  if (/menu|arrow|chevron|back|home|hamburger/.test(n)) cats.nav.push(icon);
  else if (/edit|delete|add|plus|close|check|copy|save|search/.test(n)) cats.action.push(icon);
  else if (/success|error|warning|info|alert/.test(n)) cats.status.push(icon);
  else if (/play|pause|volume|fullscreen/.test(n)) cats.media.push(icon);
  else cats.other.push(icon);
});
({ nav: cats.nav.length, action: cats.action.length, status: cats.status.length, media: cats.media.length, other: cats.other.length, details: cats });
```

### Find Icon by Context

```javascript
function findIcon(searchText) {
  const el = [...document.querySelectorAll('button, a')].find(e =>
    e.textContent?.toLowerCase().includes(searchText) ||
    e.getAttribute('aria-label')?.toLowerCase().includes(searchText)
  );
  const svg = el?.querySelector('svg');
  return svg ? { svg: svg.outerHTML, viewBox: svg.getAttribute('viewBox') } : null;
}
// findIcon('close'), findIcon('menu'), findIcon('search')
```

---

## 9. extract-interactive

**Output:** `references/interactivity.md`

### Dropdown States

```javascript
// Step 1: Extract closed state
const dropdown = document.querySelector('[class*="dropdown"], [class*="select"]');
const closedState = dropdown ? getStyles(dropdown) : null;

// Step 2: Click to open, then run:
const openDropdown = document.querySelector('[class*="dropdown"][class*="open"], [class*="menu"]:not([style*="display: none"])');
const openState = openDropdown ? getStyles(openDropdown) : null;
const optionHover = openDropdown?.querySelector('[class*="option"]:hover, [class*="item"]:hover');

({ closed: closedState, open: openState, optionHover: optionHover ? getStyles(optionHover) : null });
```

### Video Player Controls

```javascript
const player = document.querySelector('video, [class*="player"], [class*="video"]');
const controls = document.querySelector('[class*="controls"]');
if (controls) ({
  container: getStyles(controls),
  playButton: getStyles(controls.querySelector('[class*="play"]')),
  timeline: getStyles(controls.querySelector('[class*="timeline"], [class*="progress"], [class*="seek"]')),
  volume: getStyles(controls.querySelector('[class*="volume"]')),
  fullscreen: getStyles(controls.querySelector('[class*="fullscreen"]'))
});
```

### Hover Effects

```javascript
// Run on a data table row
function captureRowHover(selector) {
  const row = document.querySelector(selector);
  if (!row) return null;
  const before = getStyles(row);
  // Simulate hover by adding class (if site uses it)
  row.classList.add('hover');
  const after = getStyles(row);
  row.classList.remove('hover');
  return { before, after, diff: diffStyles(before, after) };
}
captureRowHover('tbody tr');
```

### Tooltip

```javascript
// Hover over element with tooltip, then:
const tooltip = document.querySelector('[role="tooltip"], [class*="tooltip"]');
if (tooltip) ({
  styles: getStyles(tooltip),
  arrow: getStyles(tooltip.querySelector('[class*="arrow"]')),
  text: tooltip.textContent?.trim()
});
```

---

## Quick Reference: Subagent → Sections

| Subagent | Sections to Copy |
|----------|------------------|
| extract-tokens | Utilities + Section 1 |
| extract-buttons | Utilities + Section 2 |
| extract-forms | Utilities + Section 3 |
| extract-navigation | Utilities + Section 4 |
| extract-cards | Utilities + Section 5 |
| extract-data-display | Utilities + Section 6 |
| extract-modals | Utilities + Section 7 |
| extract-icons | Section 8 (no utilities needed) |
| extract-interactive | Utilities + Section 9 |
