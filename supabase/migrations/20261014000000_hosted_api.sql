-- State for the hosted API. Only the server (service-role key) reads and writes:
-- RLS is on for every table and there are no policies, so the anon and authenticated roles see nothing.

create table api_keys (
  key_hash    text primary key,                 -- sha256 of the key, never the raw key
  email       text not null,
  created_at  timestamptz not null default now(),
  daily_limit integer not null default 50,
  active      boolean not null default true
);

create table queries (
  id               bigint generated always as identity primary key,
  key_hash         text not null references api_keys (key_hash),
  query            text not null,
  created_at       timestamptz not null default now(),
  latency_ms       integer,
  scoring_cost_usd numeric,
  result_count     integer
);
create index queries_key_day on queries (key_hash, created_at);

create table page_usage (
  url     text primary key,
  fetched integer not null default 0,
  cited   integer not null default 0
);

create table domain_usage (
  domain  text primary key,
  fetched integer not null default 0,
  cited   integer not null default 0
);

create table api_cache (
  service      text not null,
  request_hash text not null,
  response     jsonb not null,
  created_at   timestamptz not null default now(),
  primary key (service, request_hash)
);

-- Not in the spec's table list: /v1/keys is limited to 3 per IP per day, and the host's
-- memory is wiped on deploy, so the count lives here. Stores a sha256 of the IP, not the IP.
create table key_requests (
  id         bigint generated always as identity primary key,
  ip_hash    text not null,
  created_at timestamptz not null default now()
);
create index key_requests_ip_day on key_requests (ip_hash, created_at);

alter table api_keys     enable row level security;
alter table queries      enable row level security;
alter table page_usage   enable row level security;
alter table domain_usage enable row level security;
alter table api_cache    enable row level security;
alter table key_requests enable row level security;
