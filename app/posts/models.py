from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(150), nullable=False)
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(
        sa.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    category: Mapped[str] = mapped_column(
        sa.Enum("news", "publication", "tech", "other", name="post_category"),
        default="other"
    )

    def __repr__(self):
        return f"<Post(title={self.title})>"