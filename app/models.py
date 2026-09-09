from sqlalchemy import BigInteger, Column, Integer, String, Boolean, ForeignKey, Text, UniqueConstraint
from .database import Base, SessionLocal
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship




class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()") )   
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False )
    owner = relationship("User")
    media = relationship(
    "Media",
    back_populates="post",
    cascade="all, delete"
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    phone_number = Column(String)

    full_name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    website = Column(String, nullable=True)

    profile_picture_size = Column(BigInteger)
    profile_picture = Column(String, nullable=True)
    profile_picture_mime = Column(String)
    

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)



class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)

    content = Column(String, nullable=False)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE")
    )

    parent_comment_id = Column(
        Integer,
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()")
    )

    owner = relationship("User")

    post = relationship("Post")

class Follows(Base):
    __tablename__ = "followers"

    __table_args__ = (
        UniqueConstraint(
            "follower_id",
            "following_id",
            name="uq_follower_following"
        ),
    )

    id = Column(Integer, primary_key=True, nullable=False)

    follower_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    following_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    follower = relationship(
        "User",
        foreign_keys=[follower_id]
    )

    following = relationship(
        "User",
        foreign_keys=[following_id]
    )


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()")
    )

    user = relationship("User")
    post = relationship("Post")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="unique_bookmark"
        ),
    )


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)

    recipient_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    actor_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    type = Column(
        String,
        nullable=False
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=True
    )

    comment_id = Column(
        Integer,
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()")
    )

    recipient = relationship("User", foreign_keys=[recipient_id])
    actor = relationship("User", foreign_keys=[actor_id])
    post = relationship("Post")
    comment = relationship("Comment")



class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, nullable=False)

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    file_url = Column(String, nullable=False)

    file_type = Column(
        String,
        nullable=False
    )
    # image
    # video

    mime_type = Column(
        String,
        nullable=False
    )
    # image/jpeg
    # image/png
    # video/mp4

    file_size = Column(
        BigInteger,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    owner = relationship("User")

    post = relationship(
        "Post",
        back_populates="media"
    )


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    file_url = Column(String)

    file_type = Column(String)

    mime_type = Column(String)

    file_size = Column(BigInteger)

    expires_at = Column(
        TIMESTAMP(timezone=True)
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()")
    )

    owner = relationship("User")




class LiveStream(Base):
    __tablename__ = "live_streams"

    id = Column(Integer, primary_key=True)

    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(String, nullable=False)

    description = Column(Text)

    category = Column(String)

    stream_key = Column(
        String,
        unique=True,
        nullable=False,
    )

    playback_url = Column(String)

    thumbnail_url = Column(String)

    recording_url = Column(String)

    status = Column(
        String,
        nullable=False,
        default="OFFLINE",
    )
    # OFFLINE
    # LIVE
    # ENDED
    # PROCESSING

    is_live = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    current_viewers = Column(
        Integer,
        default=0,
        nullable=False,
    )

    peak_viewers = Column(
        Integer,
        default=0,
        nullable=False,
    )

    started_at = Column(
        TIMESTAMP(timezone=True),
    )

    ended_at = Column(
        TIMESTAMP(timezone=True),
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    owner = relationship("User")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    sender_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    receiver_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    message = Column(Text, nullable=False)

    is_read = Column(Boolean, server_default="false")

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )

    sender = relationship(
        "User",
        foreign_keys=[sender_id]
    )

    receiver = relationship(
        "User",
        foreign_keys=[receiver_id]
    )

