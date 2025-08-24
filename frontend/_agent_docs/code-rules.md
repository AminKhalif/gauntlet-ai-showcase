# Frontend Code Rules (Next.js App Router)

You are an expert in TypeScript, Next.js App Router, React, shadcn/ui, Radix UI, Tailwind.

## AI-First Compatibility

ALWAYS keep files under 500 lines.
ALWAYS use @fileoverview at the top of a file to summarize its contents.
ALWAYS use descriptive file and function names.
ALWAYS use descriptive block comments for functions (JSDoc block w/ @description).
ALWAYS use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError).

## Code Style and Structure

Write concise, technical code.
Use functional and declarative programming patterns; avoid classes.
Prefer iteration and modularization over code duplication (DRY methods).
Throw errors instead of adding fallback values.

## Commands
- Dev: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`
- Typecheck: `npm run typecheck`

Use npm only.

## Repo Scope
Work only in `frontend/src/**`.

Don't modify `components/ui/**` (shadcn components).
Only change `package.json` or `next.config.mjs` for specific dependency/config tasks.

## File Structure
```
src/
├── app/          # Routes, layouts, Server Components by default
├── components/   # React components
│   ├── ui/      # shadcn (read-only)
│   ├── layout/  # Navigation, headers
│   └── workflow/ # Domain components
├── hooks/        # Custom hooks
├── lib/          # Utils, helpers, constants
└── types/        # Shared types only
```

## Naming Conventions
- Components: `PascalCase.tsx`
- Hooks: `useThing.ts`
- Utils: `kebab-case.ts`
- Types: colocate as `Component.types.ts` when local
- Variables: descriptive with auxiliary verbs (`isLoading`, `hasError`, `shouldRender`)

## Required Headers
```tsx
/**
 * @fileoverview Brief description of what this file does specifically.
 */
```

## Function Documentation
```tsx
/**
 * @description Clear explanation of what this function does.
 */
export function getBuilderInitials(name: string): string {
  return name.split(" ").map(s => s[0]).join("").slice(0, 2).toUpperCase()
}
```

## TypeScript Rules
Avoid `any`. Use proper types or `unknown` with narrowing.

```tsx
import type React from "react"
import type { Metadata } from "next"

type ComponentProps = {
  title: string
  isVisible: boolean
  onClose?: () => void
}
```

## Component Patterns

Default to Server Components. Use `"use client"` only when you need state, effects, or browser APIs.

```tsx
/**
 * @fileoverview Server component for displaying builder workflow data.
 */

export default async function BuilderPage() {
  const workflowData = await fetchWorkflowData()
  return <WorkflowDisplay data={workflowData} />
}
```

```tsx
/**
 * @fileoverview Interactive modal component with form state.
 */

"use client"

import { useState } from "react"

type ModalProps = {
  isOpen: boolean
  onClose: () => void
}

/**
 * @description Modal component for adding new builder with form validation.
 */
export function AddBuilderModal({ isOpen, onClose }: ModalProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  const handleSubmit = () => {
    if (!formData.name) throw new Error("Name is required")
    // Handle submission
  }
  
  return <Dialog open={isOpen} onOpenChange={onClose}>
    {/* Modal content */}
  </Dialog>
}
```

## Data Flow
- Fetch on server using `fetch` with Next.js caching
- Use Server Actions for mutations with Zod validation
- Pass data via props, not direct imports
- Complex logic goes in custom hooks

## Import Order
1. React and Next.js
2. Third-party libraries
3. Absolute project imports (`@/`)
4. Relative imports

## State Management
- Local state: `useState`, `useReducer`
- Complex async state: TanStack Query or Zustand when needed
- Forms: React Hook Form + Zod

## Error Handling
Throw errors instead of fallback values:
```tsx
// Good
if (!workflow) throw new Error("Workflow not found")

// Bad  
const workflow = data || {}
```

Prefer route-level error boundaries:
- `loading.tsx` for loading UI
- `error.tsx` for error boundaries
- `not-found.tsx` for 404s

## Performance
- Use `next/image` and `next/font`
- Use `dynamic()` for code-splitting large client components
- Stable keys in lists

## Quality Gates
Before committing:
- `npm run lint` passes
- `npm run typecheck` passes
- `npm run build` succeeds