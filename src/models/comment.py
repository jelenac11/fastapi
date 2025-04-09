import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

if TYPE_CHECKING:
    from models import Post, User


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    post_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("post.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")

    def __repr__(self) -> str:
        return f"<Comment id={self.id} post_id={self.post_id} user_id={self.user_id}>"
