# Interactive Patterns

Patterns for making dashboards interactive, filterable, and useful.

## Filtering

### Toggle Groups (Mutually Exclusive)
```css
.toggle-group {
  display: inline-flex;
  background-color: #f5f5f5;
  padding: 0.25rem;
  border-radius: 0.375rem;
  gap: 0.125rem;
}

.toggle-button {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  background: transparent;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  color: #737373;
  transition: all 0.15s ease;
}

.toggle-button.active {
  background-color: white;
  color: #171717;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}
```

```html
<div class="toggle-group">
  <button class="toggle-button active">Weekly</button>
  <button class="toggle-button">Monthly</button>
  <button class="toggle-button">All Time</button>
</div>
```

### Checkbox Filters (Multi-Select)
```css
.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.filter-checkbox input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
  border-radius: 0.25rem;
  border: 1px solid #d4d4d4;
  cursor: pointer;
}

.filter-checkbox input[type="checkbox"]:checked {
  background-color: #171717;
  border-color: #171717;
}
```

```html
<div class="filter-group">
  <label class="filter-checkbox">
    <input type="checkbox" checked> Active
  </label>
  <label class="filter-checkbox">
    <input type="checkbox" checked> Inactive
  </label>
  <label class="filter-checkbox">
    <input type="checkbox"> Archived
  </label>
</div>
```

## Sorting

### Sortable Table Headers
```css
th.sortable {
  cursor: pointer;
  user-select: none;
}

th.sortable:hover {
  background-color: #f0f0f0;
}

th.sortable::after {
  content: '';
  margin-left: 0.5rem;
  opacity: 0.3;
}

th.sort-asc::after { content: '↑'; opacity: 1; }
th.sort-desc::after { content: '↓'; opacity: 1; }
```

```html
<th class="sortable sort-desc">Name</th>
<th class="sortable">Date</th>
<th class="sortable">Count</th>
```

### JavaScript Pattern
```javascript
function sortTable(column, direction) {
  const rows = Array.from(document.querySelectorAll('tbody tr'));
  rows.sort((a, b) => {
    const aVal = a.querySelector(`td[data-column="${column}"]`).textContent;
    const bVal = b.querySelector(`td[data-column="${column}"]`).textContent;
    return direction === 'asc'
      ? aVal.localeCompare(bVal)
      : bVal.localeCompare(aVal);
  });
  const tbody = document.querySelector('tbody');
  rows.forEach(row => tbody.appendChild(row));
}
```

## Hover Effects

### Row Highlighting
```css
tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background-color: #fafafa;
}
```

### Cell Selection
```css
.data-cell {
  cursor: pointer;
  transition: all 0.15s ease;
}

.data-cell:hover {
  background-color: #f5f5f5;
}

.data-cell.selected {
  box-shadow: inset 0 0 0 2px #171717;
}
```

## Linking to Context

### Always Provide Links
Every data point should link to its source or related admin tool:

```html
<!-- Link to admin/detail view -->
<td>
  <a href="/admin/users/12345" class="entity-link">John Doe</a>
</td>

<!-- Link to external tool -->
<td>
  <a href="https://admin.example.com/team/789" target="_blank" class="entity-link">
    Team Name ↗
  </a>
</td>
```

```css
.entity-link {
  color: #171717;
  text-decoration: none;
  border-bottom: 1px dashed #d4d4d4;
}

.entity-link:hover {
  border-bottom-style: solid;
  color: #525252;
}
```

### Contextual Actions
```html
<td class="actions">
  <a href="/view/123" title="View details">👁</a>
  <a href="/edit/123" title="Edit">✏️</a>
  <a href="/admin/123" title="Admin panel">⚙️</a>
</td>
```

## Loading States

### Skeleton Loaders
```css
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e5e5e5 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 0.25rem;
}

.skeleton-text {
  height: 1rem;
  width: 100%;
}

.skeleton-cell {
  height: 2.5rem;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Loading Overlay
```css
.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}
```

## Tooltips

```css
.tooltip-trigger {
  position: relative;
  cursor: help;
}

.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  padding: 0.5rem 0.75rem;
  background: #171717;
  color: white;
  font-size: 0.75rem;
  border-radius: 0.375rem;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: all 0.15s ease;
}

.tooltip-trigger:hover .tooltip {
  opacity: 1;
  visibility: visible;
}
```

## Data Refresh

### Last Updated Indicator
```html
<div class="last-updated">
  <span class="muted">Last updated:</span>
  <span id="update-time">January 15, 2025 at 3:45 PM</span>
  <button class="btn-secondary btn-small" onclick="refreshData()">
    ↻ Refresh
  </button>
</div>
```

## Best Practices

1. **Make everything clickable** - If data has a detail view, link to it
2. **Show filter state** - Always show what filters are active
3. **Provide feedback** - Show loading states during operations
4. **Enable exploration** - Allow sorting, filtering, drilling down
5. **Link to admin** - Every entity should link to its management interface
6. **Remember state** - Persist filter/sort preferences in URL or localStorage
7. **Keyboard accessible** - Support Tab navigation, Enter to activate
