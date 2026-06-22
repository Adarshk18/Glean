import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary key - a randomly generated UUID, created in Python
    # (default=uuid.uuid4) rather than relying on the database to
    # generate it.
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Login identifier. unique=True creates a database-level constraint -
    # Postgres itself will reject a second row with the same email, which
    # is a stronger guarantee than only checking in Python before insert
    # (avoids a race condition where two signups happen at the exact same
    # moment).
    email = Column(String, unique=True, index=True, nullable=False)

    # Bcrypt hash of the user's password. NEVER store the plain password.
    # The actual hashing logic lives in app/core/security.py (added later).
    hashed_password = Column(String, nullable=False)

    # Audit field: when the account was created.
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # -------------------------------------------------------------
    # Relationship (not a real column): lets us write `user.documents`
    # in Python to get every Document this user owns. The actual foreign
    # key lives on the Document model (defined in document.py).
    # "cascade=all, delete-orphan" means: if a User row is deleted, all
    # their Documents are automatically deleted too (no orphaned data).
    # -------------------------------------------------------------
    documents = relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"