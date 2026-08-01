# Database Schema

MySQL 8, InnoDB, `utf8mb4`. Managed via Flask-Migrate (Alembic) —
`backend/migrations/`. `deployment/mysql/schema.sql` mirrors the same schema
for bootstrapping a fresh VM3 without running migrations first.

## `urls`

| Column | Type | Notes |
|---|---|---|
| id | INT, PK, auto-increment | |
| short_code | VARCHAR(16) | Unique, indexed. 7-char base62 by default (`SHORT_CODE_LENGTH`) |
| original_url | VARCHAR(2048) | The destination URL |
| original_url_hash | CHAR(64) | SHA-256 hex digest of `original_url`, unique + indexed. Used to detect duplicate submissions in O(1) instead of scanning/comparing the full URL column |
| total_clicks | INT | Denormalized counter, incremented on each redirect |
| created_at | DATETIME | Set on insert |
| last_accessed_at | DATETIME, nullable | Set on first/each redirect |

## `clicks`

One row per redirect, for analytics drill-down beyond the `total_clicks`
counter.

| Column | Type | Notes |
|---|---|---|
| id | INT, PK, auto-increment | |
| url_id | INT, FK → urls.id, ON DELETE CASCADE | Indexed |
| ip_address | VARCHAR(45), nullable | Supports IPv4 and IPv6; taken from `X-Forwarded-For` (set by Nginx) or the direct peer address |
| user_agent | VARCHAR(256), nullable | Truncated to 256 chars |
| accessed_at | DATETIME | Indexed |

## Indexing rationale

- `urls.short_code` unique index — every redirect does a point lookup on
  this column.
- `urls.original_url_hash` unique index — enforces "prevent duplicate URLs"
  and makes the duplicate check a fast indexed lookup rather than a full
  scan/compare on a 2048-char column (which also can't be uniquely indexed
  directly under MySQL's key-length limits).
- `clicks.url_id` index — supports fetching all clicks for a given short URL.
- `clicks.accessed_at` index — supports time-range analytics queries.

## Migrations

```bash
cd backend
flask db upgrade        # apply migrations (run on deploy)
flask db migrate -m "…" # generate a new migration after changing models.py
```
