from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .crud import public_profile
from . import fastapi_deps
from . import schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.PublicProfile])
async def list_public_profiles(db: Session = Depends(fastapi_deps.get_db)) -> List[schemas.PublicProfile]:
    return public_profile.list(db=db)
