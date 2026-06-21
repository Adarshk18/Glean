import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from app.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"), index=True, nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    tool_calls = Column(JSON, nullable=True)
    tool_call_id = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(
        timezone.utc), nullable=False)

    def __repr__(self) -> str:
        return f"<ChatMessage id={self.id} role={self.role} conversation_id={self.conversation_id}>"
