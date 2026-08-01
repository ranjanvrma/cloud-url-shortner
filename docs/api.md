# API Documentation

Base path: `/api` (proxied through VM1's Nginx). All responses are JSON.

## POST /api/shorten

Create a short code for a URL, or return the existing one if the same URL
was already shortened.

**Request body**

```json
{ "url": "https://example.com/some/long/path" }
```

**Responses**

| Status | Meaning |
|---|---|
| 201 | New short code created |
| 200 | URL was already shortened; existing entry returned |
| 400 | Missing/invalid JSON body, or URL failed validation |
| 429 | Rate limit exceeded (default: 20 requests/minute/IP, see `RATE_LIMIT_SHORTEN`) |

**201/200 body**

```json
{
  "short_code": "aB3xY9z",
  "short_url": "http://your-domain/aB3xY9z",
  "original_url": "https://example.com/some/long/path",
  "total_clicks": 0,
  "created_at": "2026-08-01T12:00:00+00:00",
  "last_accessed_at": null
}
```

**400 body**

```json
{ "error": "URL must start with http:// or https://" }
```

**Validation rules**: URL is required, non-empty, at most 2048 characters,
and must be an absolute `http://` or `https://` URL with a host (rejects
things like `javascript:`, `ftp://`, or bare strings).

## GET /api/stats/<short_code>

Fetch click analytics for an existing short code.

**Responses**

| Status | Meaning |
|---|---|
| 200 | Found — same body shape as the shorten endpoint |
| 404 | No URL with this short code |

## GET /<short_code>

Not under `/api` — this is the redirect endpoint used by end users. On a
match it records a click (increments `total_clicks`, sets
`last_accessed_at`, and inserts a `clicks` row with IP/User-Agent) and
responds `302 Found` with `Location` set to the original URL. Returns 404 if
the code doesn't exist.
