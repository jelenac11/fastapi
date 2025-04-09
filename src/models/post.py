import uuid
from typing import List
from models.post_tag_association import post_tag_association
from models.base import Base
from models.enums import PostStatus
from models.tag import Tag
from models.user import User
from models.comment import Comment
from sqlalchemy import String, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Post(Base):
    __tablename__ = "post"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PostStatus] = mapped_column(Enum(PostStatus), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped[User] = relationship(back_populates="posts")
    comments: Mapped[List[Comment]] = relationship(back_populates="post", cascade="all, delete-orphan")
    tags: Mapped[List[Tag]] = relationship(secondary=post_tag_association, back_populates="posts")

    def __repr__(self) -> str:
        return f"<Post id={self.id} title={self.title!r} status={self.status!r}>"
