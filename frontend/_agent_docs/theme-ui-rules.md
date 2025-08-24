# Frontend Theme & UI Rules

**Purpose:** Keep your design consistent and prevent random colors/styling.

## Colors (Zinc-based only)
- Text: `text-zinc-900` (headings), `text-zinc-600` (descriptions), `text-zinc-500` (labels)
- Backgrounds: `bg-white` (cards), `bg-zinc-50` (subtle areas)
- Buttons: `bg-zinc-900` (primary), `variant="ghost"` (secondary)
- Borders: `border-zinc-200`

Don't use random colors like purple, blue, green.

## Common Patterns

### Cards
```tsx
// Main cards
<Card className="border-zinc-200 bg-white p-6">

// Nested cards (inside other cards)
<Card className="border-zinc-200/50 bg-zinc-50/50 p-3">
```

### Buttons
```tsx
// Primary actions
<Button className="bg-zinc-900 hover:bg-zinc-800">Add Builder</Button>

// Secondary actions  
<Button variant="ghost" className="text-zinc-600 hover:text-zinc-900">
```

### Text Sizes
- Headlines: `text-3xl font-bold text-zinc-900`
- Sections: `text-lg font-semibold text-zinc-900`
- Body: `text-sm text-zinc-600`
- Labels: `text-xs text-zinc-500`

## Layout
- Page containers: `max-w-6xl mx-auto px-4`
- Card spacing: `space-y-3` or `gap-6`
- Mobile responsive: `md:text-4xl`, `sm:grid-cols-2`

## Interactive States
Always include hover states on clickable elements.
Use `transition-colors` for smooth changes.