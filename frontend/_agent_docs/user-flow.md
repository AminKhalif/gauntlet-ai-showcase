# User Flow & Navigation Rules

**Purpose:** Define how users navigate through the app and ensure consistent routing patterns.

## App Routes & Navigation

### Main Flow
1. **Homepage** (`/`) - Builder showcase grid
2. **Individual Builder** (`/builders/[slug]`) - Detailed workflow view  
3. **How It Works** (`/how-it-works`) - Explanation page
4. **Add Builder Modal** - Overlay form (not a route)

### URL Structure
- `/` - Homepage with all builders
- `/builders/jane-cooper` - Individual builder page (slug-based)
- `/how-it-works` - Static explanation page

## Navigation Components

### Top Navigation (`TopNav`)
- Brand logo: links to `/` 
- "Builders" link: goes to `/`
- "How it Works" link: goes to `/how-it-works`
- "Add Builder" button: opens modal overlay

### Mobile Navigation
- Hamburger menu for mobile
- Same links as desktop
- Modal opens and closes mobile menu

## User Actions & States

### Homepage Interactions
- Click builder card → navigate to `/builders/[slug]`
- Click "Add Builder" → open modal
- Search/filter builders (future feature)

### Builder Page Interactions  
- Phase navigation: scroll or tab between sections
- Expand/collapse practices within phases
- Quote playback (future: link to timestamp in source video)
- "Add Builder" still accessible in nav

### Modal Interactions
- Form submission → process data, close modal
- Cancel → close modal, stay on current page
- "How it Works" link → open in new tab

## Loading & Error States

### Page Loading
- Use Next.js `loading.tsx` for route-level loading
- Show skeleton for builder cards while loading
- Handle empty states (no builders found)

### Error Handling  
- Use `error.tsx` for route-level errors
- `not-found.tsx` for invalid builder slugs
- Form validation errors inline

### Navigation States
- Active link highlighting in navigation
- Mobile menu open/closed states
- Modal open/closed states

## Future Navigation Considerations
- Search/filtering on homepage
- Categories or tags for builders
- Pagination if many builders
- User authentication (if needed)
- Admin interface for managing builders