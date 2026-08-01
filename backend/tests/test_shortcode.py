from app.utils.shortcode import generate_short_code, hash_url


def test_generate_short_code_length():
    code = generate_short_code(7)
    assert len(code) == 7


def test_generate_short_code_charset():
    code = generate_short_code(100)
    assert all(c.isalnum() for c in code)


def test_hash_url_deterministic():
    assert hash_url("https://example.com") == hash_url("https://example.com")


def test_hash_url_differs_for_different_input():
    assert hash_url("https://example.com/a") != hash_url("https://example.com/b")
