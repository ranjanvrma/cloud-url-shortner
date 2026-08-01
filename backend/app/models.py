from datetime import datetime, timezone

from app.extensions import db


def utcnow():
    return datetime.now(timezone.utc)


class URL(db.Model):
    __tablename__ = "urls"

    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    original_url = db.Column(db.String(2048), nullable=False)
    original_url_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    total_clicks = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=utcnow)
    last_accessed_at = db.Column(db.DateTime, nullable=True)

    clicks = db.relationship(
        "Click", backref="url", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self, base_url):
        return {
            "short_code": self.short_code,
            "short_url": f"{base_url}/{self.short_code}",
            "original_url": self.original_url,
            "total_clicks": self.total_clicks,
            "created_at": self.created_at.isoformat(),
            "last_accessed_at": self.last_accessed_at.isoformat()
            if self.last_accessed_at
            else None,
        }


class Click(db.Model):
    __tablename__ = "clicks"

    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(
        db.Integer, db.ForeignKey("urls.id", ondelete="CASCADE"), nullable=False, index=True
    )
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(256), nullable=True)
    accessed_at = db.Column(db.DateTime, nullable=False, default=utcnow, index=True)
