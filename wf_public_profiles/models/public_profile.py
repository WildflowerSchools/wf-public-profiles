from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from wf_public_profiles.db.base_class import Base


class PublicProfile(Base):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    holaspirit_id = Column(String, index=True)
    name = Column(String)
    role = Column(String)
    img_url = Column(String)
    bio = Column(String)
