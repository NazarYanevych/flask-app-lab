import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(sa.String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def hash_password(self, raw_password: str | None = None) -> None:
        password_to_hash = raw_password if raw_password is not None else self.password
        self.password = bcrypt.generate_password_hash(password_to_hash).decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"User('{self.email}')"