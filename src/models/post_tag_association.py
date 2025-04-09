from sqlalchemy import Column, ForeignKey, Table

from models.base import Base

post_tag_association = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)
