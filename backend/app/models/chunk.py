import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from app.database import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey(
        "documents.id", ondelete="CASCADE"), index=True, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    vector_id = Column(String, nullable=False, unique=True, index=True)
    token_count = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), nullable=False)
    document = relationship(
        "Document", backup_populates="owner")
    

    def __repr__(self) -> str:
        return f"<Chunk id={self.id} document_id={self.document_id} index={self.chunk_index}>"
