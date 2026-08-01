from flask import Blueprint, abort, current_app, redirect, request

from app.extensions import db
from app.models import Click, URL, utcnow

redirect_bp = Blueprint("redirect", __name__)


@redirect_bp.get("/<string:short_code>")
def redirect_to_original(short_code):
    entry = URL.query.filter_by(short_code=short_code).first()
    if entry is None:
        abort(404)

    now = utcnow()
    entry.total_clicks += 1
    entry.last_accessed_at = now

    click = Click(
        url_id=entry.id,
        ip_address=request.headers.get("X-Forwarded-For", request.remote_addr),
        user_agent=request.headers.get("User-Agent", "")[:256],
        accessed_at=now,
    )
    db.session.add(click)
    db.session.commit()

    current_app.logger.info("Redirected %s -> %s", short_code, entry.original_url)
    return redirect(entry.original_url, code=302)
