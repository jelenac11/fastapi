import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.post_tag_association import post_tag_association

if TYPE_CHECKING:
    from models import Post


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tag_association,
        back_populates="tags",
    )

    def __repr__(self) -> str:
        return f"<Tag id={self.id} name={self.name!r}>"
