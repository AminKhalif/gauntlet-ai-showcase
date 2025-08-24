# Database Setup

## Quick Setup (5 minutes)

1. **Go to your Supabase project dashboard**
2. **Click "SQL Editor" in the sidebar**
3. **Copy the contents of `schema.sql`**
4. **Paste into the SQL Editor**
5. **Click "Run" button**

That's it! Your database tables are ready.

## What Gets Created

- `builders` - Main table for builder profiles
- `workflow_cards` - 6 workflow cards per builder  
- `processing_jobs` - Async job status tracking

## Environment Variables Needed

Add these to your `.env` file:

```
SUPABASE_URL=your_project_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

Get these from: Supabase Dashboard → Settings → API