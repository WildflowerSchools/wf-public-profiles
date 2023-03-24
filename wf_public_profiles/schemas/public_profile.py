from datetime import datetime

from typing import Optional

from pydantic import BaseModel


# Shared properties
class PublicProfileBase(BaseModel):
    holaspirit_id: str
    name: str
    role: Optional[str] = None
    img_url: Optional[str] = None
    bio: Optional[str] = None


# Properties to receive on item creation
class PublicProfileCreate(PublicProfileBase):
    pass


# Properties to receive on item update
class PublicProfileUpdate(PublicProfileBase):
    pass


# Properties shared by models stored in DB
class PublicProfileInDBBase(PublicProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class PublicProfile(PublicProfileInDBBase):
    pass


# Additional properties stored in DB
class PublicProfileInDB(PublicProfileInDBBase):
    pass
