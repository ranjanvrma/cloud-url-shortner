import json


def test_shorten_creates_url(client):
    resp = client.post("/api/shorten", json={"url": "https://example.com/page"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["original_url"] == "https://example.com/page"
    assert len(body["short_code"]) == 7
    assert body["short_url"] == f"http://testserver/{body['short_code']}"
    assert body["total_clicks"] == 0


def test_shorten_duplicate_returns_same_code(client):
    first = client.post("/api/shorten", json={"url": "https://example.com/dup"})
    second = client.post("/api/shorten", json={"url": "https://example.com/dup"})
    assert first.status_code == 201
    assert second.status_code == 200
    assert first.get_json()["short_code"] == second.get_json()["short_code"]


def test_shorten_rejects_invalid_url(client):
    resp = client.post("/api/shorten", json={"url": "not-a-url"})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_shorten_rejects_missing_body(client):
    resp = client.post(
        "/api/shorten", data="not json", content_type="application/json"
    )
    assert resp.status_code == 400


def test_shorten_rejects_xss_payload_as_invalid_url(client):
    resp = client.post(
        "/api/shorten", json={"url": "<script>alert(1)</script>"}
    )
    assert resp.status_code == 400


def test_redirect_increments_clicks_and_sets_last_accessed(client):
    created = client.post("/api/shorten", json={"url": "https://example.com/redir"})
    code = created.get_json()["short_code"]

    resp = client.get(f"/{code}", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"] == "https://example.com/redir"

    stats = client.get(f"/api/stats/{code}").get_json()
    assert stats["total_clicks"] == 1
    assert stats["last_accessed_at"] is not None


def test_redirect_unknown_code_returns_404(client):
    resp = client.get("/doesnotexist123")
    assert resp.status_code == 404


def test_stats_unknown_code_returns_404(client):
    resp = client.get("/api/stats/doesnotexist")
    assert resp.status_code == 404


def test_records_click_ip_and_user_agent(client, app):
    from app.models import Click

    created = client.post("/api/shorten", json={"url": "https://example.com/track"})
    code = created.get_json()["short_code"]

    client.get(f"/{code}", headers={"User-Agent": "pytest-agent"})

    with app.app_context():
        click = Click.query.first()
        assert click is not None
        assert click.user_agent == "pytest-agent"
        assert click.ip_address is not None
