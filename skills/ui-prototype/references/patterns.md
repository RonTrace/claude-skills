# Prototype Patterns

Common patterns for interactive prototypes. Reference as needed.

## Table of Contents
- [State Controls](#state-controls)
- [Feed/List Patterns](#feedlist-patterns)
- [Bottom Sheets](#bottom-sheets)
- [Navigation Patterns](#navigation-patterns)
- [Empty States](#empty-states)
- [Loading States](#loading-states)
- [Interaction Feedback](#interaction-feedback)

---

## State Controls

### Multi-Phase Toggle

```html
<div class="control-section">
    <h3>Phase</h3>
    <div class="control-row">
        <button class="control-btn active" data-phase="pre">Pre</button>
        <button class="control-btn" data-phase="live">Live</button>
        <button class="control-btn" data-phase="post">Post</button>
    </div>
</div>
```

```javascript
document.querySelectorAll('[data-phase]').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('[data-phase]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.phase = btn.dataset.phase;
        updateUI();
    });
});
```

### Data Density

```html
<div class="control-section">
    <h3>Data</h3>
    <div class="control-row">
        <button class="control-btn" data-density="empty">Empty</button>
        <button class="control-btn active" data-density="normal">Normal</button>
        <button class="control-btn" data-density="busy">Busy</button>
    </div>
</div>
```

---

## Feed/List Patterns

### Card-Based Feed (Pinterest-style)

```css
.feed {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.feed-card {
    background: var(--card);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
    overflow: hidden;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.feed-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.feed-card:active {
    transform: scale(0.98);
}
```

### Timeline Feed (Apple-style)

```css
.timeline-item {
    display: flex;
    padding: 0 20px;
}

.time-col {
    width: 48px;
    flex-shrink: 0;
    padding-top: 12px;
}

.time-text {
    font-size: 11px;
    font-weight: 500;
    color: var(--muted-foreground);
}

.content-col {
    flex: 1;
    border-left: 1px solid var(--border);
    padding: 12px 0 12px 16px;
}

.timeline-item:last-child .content-col {
    border-left-color: transparent;
}
```

### List with Dividers

```css
.list-item {
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 12px;
}

.list-item:last-child {
    border-bottom: none;
}

.list-item:active {
    background: var(--muted);
}
```

---

## Bottom Sheets

### Slide-up Sheet

```css
.sheet-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.3);
    z-index: 199;
    opacity: 1;
    transition: opacity 0.3s ease;
}

.sheet-backdrop.hidden {
    opacity: 0;
    pointer-events: none;
}

.sheet {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 390px; /* match phone frame */
    background: var(--card);
    border-radius: 20px 20px 0 0;
    padding: 20px;
    box-shadow: 0 -10px 40px rgb(0 0 0 / 0.15);
    z-index: 200;
    transition: transform 0.3s ease;
}

.sheet.hidden {
    transform: translate(-50%, 100%);
}

.sheet-handle {
    width: 36px;
    height: 4px;
    background: var(--gray-300);
    border-radius: 2px;
    margin: 0 auto 16px;
}
```

```javascript
function showSheet() {
    document.getElementById('sheet').classList.remove('hidden');
    document.getElementById('sheet-backdrop').classList.remove('hidden');
}

function hideSheet() {
    document.getElementById('sheet').classList.add('hidden');
    document.getElementById('sheet-backdrop').classList.add('hidden');
}

document.getElementById('sheet-backdrop').addEventListener('click', hideSheet);
```

---

## Navigation Patterns

### Tab Bar

```css
.tab-bar {
    display: flex;
    border-top: 1px solid var(--border);
    background: var(--background);
}

.tab-item {
    flex: 1;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    color: var(--muted-foreground);
    cursor: pointer;
}

.tab-item.active {
    color: var(--btn-primary);
}

.tab-icon { font-size: 20px; }
.tab-label { font-size: 10px; font-weight: 500; }
```

### Segmented Control

```css
.segmented {
    display: flex;
    background: var(--muted);
    border-radius: var(--radius);
    padding: 4px;
}

.segment {
    flex: 1;
    padding: 8px 12px;
    border-radius: calc(var(--radius) - 2px);
    font-size: 13px;
    font-weight: 500;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
}

.segment.active {
    background: var(--card);
    box-shadow: var(--shadow);
}
```

---

## Empty States

### Centered Empty

```css
.empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
    text-align: center;
}

.empty-icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.4;
}

.empty-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 8px;
}

.empty-text {
    font-size: 14px;
    color: var(--muted-foreground);
    line-height: 1.5;
}
```

### Inline Prompt

```css
.prompt-card {
    background: var(--gray-50);
    border: 1px dashed var(--border);
    border-radius: var(--radius-lg);
    padding: 24px;
    text-align: center;
}

.prompt-text {
    font-size: 14px;
    color: var(--muted-foreground);
    margin-bottom: 12px;
}
```

---

## Loading States

### Skeleton

```css
.skeleton {
    background: linear-gradient(
        90deg,
        var(--gray-200) 25%,
        var(--gray-100) 50%,
        var(--gray-200) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: var(--radius);
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.skeleton-text { height: 14px; width: 60%; }
.skeleton-title { height: 20px; width: 40%; }
.skeleton-avatar { width: 40px; height: 40px; border-radius: 50%; }
```

### Spinner

```css
.spinner {
    width: 24px;
    height: 24px;
    border: 2px solid var(--border);
    border-top-color: var(--btn-primary);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
```

---

## Interaction Feedback

### Button Press

```css
.btn:active {
    transform: scale(0.97);
}
```

### Tap Highlight

```css
.tappable {
    -webkit-tap-highlight-color: transparent;
    transition: background 0.1s ease;
}

.tappable:active {
    background: var(--muted);
}
```

### Reaction Animation

```javascript
function animateReaction(btn) {
    btn.style.transform = 'scale(1.2)';
    setTimeout(() => {
        btn.style.transform = '';
    }, 150);
}
```

### Pulse Animation (Live Indicator)

```css
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.live-dot {
    width: 6px;
    height: 6px;
    background: #ef4444;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}
```
