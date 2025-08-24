-- AI Workflow Showcase Database Schema
-- Paste this into your Supabase SQL Editor and click "Run"

-- builders hold metadata and a pointer to the GCS audio
create table if not exists builders (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text unique not null,
  youtube_url text not null,
  avatar_url text,
  gcs_audio_blob_name text,
  gcs_audio_url text,
  audio_duration_seconds real,
  status text default 'pending',             -- pending, processing, completed, failed
  created_at timestamptz default now()
);

-- one row per workflow card
create table if not exists workflow_cards (
  id uuid primary key default gen_random_uuid(),
  builder_id uuid references builders(id) on delete cascade,
  card_type text not null,                   -- planning, context, codegen, verification, iteration, delivery
  summary text not null,
  workflow_json jsonb,                       -- keep full structured output for now
  created_at timestamptz default now(),
  unique(builder_id, card_type)
);

-- optional progress tracking
create table if not exists processing_jobs (
  id uuid primary key default gen_random_uuid(),
  builder_id uuid references builders(id) on delete cascade,
  status text default 'pending',
  current_stage text,                        -- downloading, transcribing, extracting
  progress_percentage int default 0,
  error_message text,
  started_at timestamptz default now(),
  completed_at timestamptz,
  metadata jsonb
);

-- indexes for performance
create index if not exists idx_builders_slug on builders(slug);
create index if not exists idx_workflow_cards_builder on workflow_cards(builder_id);
create index if not exists idx_processing_jobs_builder on processing_jobs(builder_id);