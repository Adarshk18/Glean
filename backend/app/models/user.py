import uuid
from datetime import datetime , timezone
from sqlalchemy import Column, String, Datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import realtionship


from app.database import Base

class User(Base):
    __tablename__ = "users"

    id=Column(UUID(as_uuid=True))
