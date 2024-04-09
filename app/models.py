from datetime import datetime
from typing import Optional, List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, sql
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
                                           nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    published: Mapped[bool] = mapped_column(Boolean, server_default='TRUE', nullable=False)
    rating: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=sql.func.now())
    author: Mapped["User"] = relationship("User", back_populates="posts")
    votes: Mapped[List["Vote"]] = relationship("Vote", back_populates="post")

    @property
    def likes(self) -> int:
        return len(self.votes)

    def __repr__(self) -> str:
        return f"<Post id={self.id} title={self.title} content={self.content} published={self.published} rating={self.rating}>"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=sql.func.now())
    posts: Mapped[List["Post"]] = relationship(back_populates="author")
    votes: Mapped[List["Vote"]] = relationship("Vote", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} name={self.name} email={self.email} created_at={self.created_at}>"


class Vote(Base):
    __tablename__ = "votes"
    user_id: Mapped[int] = mapped_column(ForeignKey(column="users.id", ondelete="CASCADE", onupdate="CASCADE"),
                                         primary_key=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", onupdate="CASCADE", ondelete="CASCADE"),
                                         primary_key=True, nullable=False)
    post: Mapped["Post"] = relationship("Post", back_populates="votes")
    user: Mapped["User"] = relationship("User", back_populates="votes")
