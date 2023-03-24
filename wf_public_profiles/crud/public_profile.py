from typing import Any, Dict, List, Optional, Type, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from wf_public_profiles.models.public_profile import PublicProfile
from wf_public_profiles.schemas.public_profile import PublicProfileCreate, PublicProfileUpdate


class CRUDPublicProfile:
    def __init__(self, model: Type[PublicProfile]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[PublicProfile]:
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[PublicProfile]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: PublicProfileCreate) -> PublicProfile:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: PublicProfile, obj_in: Union[PublicProfileUpdate, Dict[str, Any]]
    ) -> PublicProfile:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> PublicProfile:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_all(self, db: Session) -> None:
        db.query(self.model).delete()
        db.commit()


public_profile = CRUDPublicProfile(PublicProfile)
