# Frontend Theme Rules — AI-Workflow-Showcase

**Purpose:** Establish consistent theming foundations for AI-first UI development. Ensures all components follow the established design system and visual identity.

## Color System

### Core Palette (Zinc-based neutral system)
```css
/* Light Mode Primary */
--background: oklch(1 0 0)           /* Pure white backgrounds */
--foreground: oklch(0.145 0 0)       /* Near-black text */
--primary: oklch(0.205 0 0)          /* Dark zinc (zinc-900) */
--primary-foreground: oklch(0.985 0 0) /* Light text on dark */

/* Secondary & Muted */
--secondary: oklch(0.97 0 0)         /* Light zinc (zinc-50) */
--muted: oklch(0.97 0 0)             /* zinc-50 for subtle backgrounds */
--muted-foreground: oklch(0.556 0 0) /* zinc-600 for secondary text */

/* Borders & Inputs */
--border: oklch(0.922 0 0)           /* zinc-200 for subtle borders */
--input: oklch(0.922 0 0)            /* zinc-200 for input borders */
--ring: oklch(0.708 0 0)             /* zinc-400 for focus rings */
```

### Usage Guidelines
- **Primary Actions:** `bg-zinc-900 hover:bg-zinc-800` (dark buttons, key CTAs)
- **Cards & Surfaces:** `bg-white border-zinc-200` with optional `/70` opacity for layering
- **Text Hierarchy:**
  - Primary: `text-zinc-900` (headings, important text)
  - Secondary: `text-zinc-600` (descriptions, metadata)
  - Muted: `text-zinc-500` (labels, timestamps)
  - Disabled: `text-zinc-400` (inactive states)

### Color Semantic Mapping
```typescript
// Use these instead of raw colors
const THEME_COLORS = {
  text: {
    primary: 'text-zinc-900',
    secondary: 'text-zinc-600', 
    muted: 'text-zinc-500',
    disabled: 'text-zinc-400'
  },
  bg: {
    primary: 'bg-white',
    subtle: 'bg-zinc-50',
    muted: 'bg-zinc-100'
  },
  border: {
    default: 'border-zinc-200',
    subtle: 'border-zinc-200/70',
    muted: 'border-zinc-100'
  }
}
```

## Typography

### Scale & Weights
```css
/* Headings */
.text-3xl md:text-4xl font-bold tracking-tight  /* Main hero headlines */
.text-xl font-semibold tracking-tight           /* Page titles, brand */
.text-lg font-semibold                         /* Section headlines */
.text-sm font-medium                           /* Component labels */

/* Body Text */
.text-lg leading-relaxed                       /* Hero descriptions */
.text-sm leading-relaxed                       /* Card descriptions */
.text-xs                                       /* Metadata, badges */
```

### Font Hierarchy Rules
1. **Hero Headlines:** 3xl/4xl, bold, tight tracking
2. **Page/Section Titles:** lg/xl, semibold 
3. **Card/Component Titles:** base/lg, semibold
4. **Body Text:** sm, regular, relaxed leading
5. **Metadata/Labels:** xs, medium weight for emphasis

## Spacing & Layout

### Container System
```css
/* Page Containers */
.mx-auto max-w-6xl px-4 py-12 md:py-16    /* Main page wrapper */
.mx-auto max-w-7xl px-4                   /* Navigation wrapper */

/* Component Spacing */
.p-4 md:p-5                              /* Card padding (responsive) */
.gap-4 md:gap-6                          /* Grid gaps */
.space-y-3                               /* Vertical component spacing */
.mt-4 md:mt-6                            /* Section breaks */
```

### Responsive Breakpoints
- `sm:` 640px+ (mobile landscape)
- `md:` 768px+ (tablet)  
- `lg:` 1024px+ (desktop)
- `xl:` 1280px+ (wide desktop)

## Component Theming Patterns

### Cards & Surfaces
```css
/* Standard card styling */
.border-zinc-200 bg-white p-6 transition-all hover:border-zinc-300 hover:shadow-sm

/* Nested/layered cards */  
.border-zinc-200/70 bg-white/70 p-4 md:p-5
.border-zinc-200/50 bg-zinc-50/50 p-3
```

### Interactive States
```css
/* Buttons */
.bg-zinc-900 hover:bg-zinc-800                    /* Primary CTA */
.text-zinc-600 hover:text-zinc-900                /* Ghost/text buttons */
.transition-colors                                 /* Smooth state changes */

/* Links & Clickable Elements */
.hover:text-zinc-700 transition-colors            /* Navigation links */
.focus-visible:ring-2                             /* Keyboard focus */
```

### Status & Feedback
```css
/* Badges & Labels */
.bg-zinc-100 text-zinc-700                       /* Secondary badge */
.border px-2 py-0.5 text-xs                      /* Outline badge */

/* Loading & Empty States */
.text-zinc-400 italic                            /* Empty state text */
.animate-pulse bg-zinc-200                       /* Loading skeleton */
```

## Dark Mode Support

The system includes full dark mode CSS custom properties but is currently light-mode focused. When implementing dark mode:

1. Use CSS custom properties instead of hardcoded colors
2. Test all interactive states in both modes
3. Ensure sufficient contrast ratios (4.5:1 minimum)
4. Use `dark:` prefixes for dark-specific overrides

## Brand Identity

### Logo/Brand Treatment
- **Brand Name:** "Flowdex" 
- **Typography:** `text-xl font-semibold tracking-tight`
- **Color:** `text-zinc-900` with `hover:text-zinc-700`
- **Positioning:** Always left-aligned in navigation

### Voice & Tone in UI
- **Concise, direct copy** ("Add Builder", not "Create New Builder Profile")
- **Technical but approachable** ("Real workflows from builders using AI tools")
- **Action-oriented** (imperatives like "Add", "View", "Collapse")