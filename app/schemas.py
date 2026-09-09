from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, conint
from datetime import datetime

#the post schema is going to be used to validate the data that is sent to the API. It is going to be used in the create_post function in main.py

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    media: list["Media"] = []

    
    model_config = ConfigDict(from_attributes=True)
    

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

#this is going to the model send to the client that requested
class UserOut(BaseModel):
    id: int
    email: EmailStr
    phone_number: str | None = None
    full_name: str | None = None
    bio: str | None = None
    location: str | None = None
    website: str | None = None

    profile_picture: str | None = None
    profile_picture_mime: str | None = None
    profile_picture_size: int | None = None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)





class Post(PostBase):
    id: int 
    created_at: datetime
    owner_id: int
    owner: UserOut  
    
    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: Post
    vote: int

    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    bio: str | None = None
    location: str | None = None
    website: str | None = None

class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    bio: str | None = None
    location: str | None = None
    website: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    full_name: str | None = None
    bio: str | None = None
    location: str | None = None
    website: str | None = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., le=1)



class CommentBase(BaseModel):
    content: str
    post_id: int
    parent_comment_id: int | None = None

    
    model_config = ConfigDict(from_attributes=True)

class CommentReply(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(CommentBase):
    post_id: int
    



class Comment(BaseModel):
    id: int
    content: str
    owner_id: int
    post_id: int
    parent_comment_id: int | None = None
    created_at: datetime

    owner: UserOut
    post: Post

    
    model_config = ConfigDict(from_attributes=True)


class FollowCreate(BaseModel):
    following_id: int

   
    model_config = ConfigDict(from_attributes=True)


class Follow(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime

    follower: UserOut
    following: UserOut

    
    model_config = ConfigDict(from_attributes=True)



class BookmarkBase(BaseModel):
    post_id: int

    model_config = ConfigDict(from_attributes=True)

class BookmarkCreate(BookmarkBase):
    pass

class Bookmark(BookmarkBase):
    id: int
    created_at: datetime

    user: UserOut
    post: Post

    model_config = ConfigDict(from_attributes=True)


class NotificationBase(BaseModel):
    type: str

    model_config = ConfigDict(from_attributes=True)

class NotificationCreate(NotificationBase):
    recipient_id: int
    post_id: int | None = None
    comment_id: int | None = None 

class Notification(NotificationBase):
    id: int
    recipient_id: int
    actor_id: int
    post_id: int | None = None
    comment_id: int | None = None
    is_read: bool
    created_at: datetime

    actor: UserOut

    model_config = ConfigDict(from_attributes=True)


class MediaBase(BaseModel):
    id: int
    post_id: int
    owner_id: int
    file_url: str
    file_type: str
    mime_type: str
    file_size: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MediaCreate(BaseModel):
    post_id: int

    model_config = ConfigDict(from_attributes=True)


class Media(MediaBase):
    id: int
    owner_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



class StoryBase(BaseModel):
    file_url: str
    file_type: str
    mime_type: str
    file_size: int

    model_config = ConfigDict(from_attributes=True)


class StoryCreate(BaseModel):
    pass


class Story(StoryBase):
    id: int
    owner_id: int
    expires_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    

class LiveStreamBase(BaseModel):
    title: str
    description: str | None = None
    category: str | None = None
    thumbnail: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LiveStreamCreate(LiveStreamBase):
    pass


class LiveStreamUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    thumbnail: str | None = None


class LiveStream(LiveStreamBase):
    id: int
    owner_id: int
    stream_key: str
    playback_url: str | None = None
    is_live: bool
    current_viewers: int = 0
    peak_viewers: int = 0
    recording_url: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    created_at: datetime
    owner: UserOut | None = None

    model_config = ConfigDict(from_attributes=True)


class LiveStreamPublish(BaseModel):
    stream_key: str
    started_at: datetime | None = None


class LiveStreamWatchResponse(BaseModel):
    stream_id: int
    playback_url: str | None = None
    is_live: bool
    stream: LiveStream


class LiveStreamChatMessage(BaseModel):
    message: str


class LiveStreamChatResponse(BaseModel):
    stream_id: int
    message: str
    sender_id: int | None = None


class LiveStreamStats(BaseModel):
    stream_id: int
    is_live: bool
    current_viewers: int = 0
    peak_viewers: int = 0
    started_at: datetime | None = None
    ended_at: datetime | None = None


class MessageBase(BaseModel):
    receiver_id: int
    message: str

class MessageCreate(MessageBase):
    pass

class MessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

