# Testing

## Backend (pytest)

```bash
cd backend
python -m venv venv
./venv/Scripts/activate       # Windows
# source venv/bin/activate    # Linux/macOS
pip install -r requirements-dev.txt
pytest -v
```

Tests use an in-memory SQLite database (`tests/conftest.py`) — no MySQL
required. Coverage includes:

- `tests/test_shortcode.py` — short code length/charset, URL hashing
- `tests/test_validators.py` — URL validation (accepts valid http/https,
  rejects empty/None/non-http schemes/oversized/malformed input)
- `tests/test_api.py` — shorten (create + duplicate detection + invalid
  input + XSS-payload rejection), redirect (click increment,
  last-accessed timestamp, IP/User-Agent recording), 404s for unknown codes
- `tests/test_rate_limit.py` — the shorten endpoint returns 429 once the
  configured limit is exceeded

## Manual end-to-end check

1. Start the backend: `cd backend && ./venv/Scripts/python wsgi.py`
   (set `SQLALCHEMY_DATABASE_URI=sqlite:///dev.db` and `BASE_URL` env vars
   for local testing without MySQL).
2. Apply migrations first: `flask db upgrade`.
3. Open `frontend/index.html` served from the same origin as the API (in
   production this is automatic via Nginx; for local testing, serve both
   through one process or point the frontend at an absolute API URL).
4. Submit a URL, confirm a short link + stats appear, click Copy, and visit
   the short link to confirm it redirects and the click count increments.

## What to verify after deploying to AWS

- `curl -X POST http://<VM1-public-ip>/api/shorten -H "Content-Type: application/json" -d '{"url":"https://example.com"}'`
- Visit the returned `short_url` in a browser and confirm the redirect.
- `curl http://<VM1-public-ip>/api/stats/<code>` shows `total_clicks: 1`.
- Confirm VM2 and VM3 are **not** reachable from the public internet
  (only from each other / VM1, per their security groups).
