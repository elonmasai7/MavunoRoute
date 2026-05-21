from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_permission
from app.schemas.crops import CropCreate, CropRead, CropUpdate
from app.services.crop_service import CropService
from app.utils.pagination import build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/crops", tags=["Crops"])


@router.post("")
def create_crop(payload: CropCreate, db: Session = Depends(get_db), _=Depends(require_permission("users:read"))):
    crop = CropService(db).create(payload)
    return success_response("Operation completed successfully", CropRead.model_validate(crop).model_dump(mode="json"))


@router.get("")
def list_crops(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    rows, total = CropService(db).list(page, per_page)
    data = [CropRead.model_validate(item).model_dump(mode="json") for item in rows]
    return success_response("Records retrieved successfully", data, build_pagination_meta(page, per_page, total))


@router.get("/{crop_id}")
def get_crop(crop_id: UUID, db: Session = Depends(get_db)):
    crop = CropService(db).get(crop_id)
    return success_response("Record retrieved successfully", CropRead.model_validate(crop).model_dump(mode="json"))


@router.patch("/{crop_id}")
def update_crop(crop_id: UUID, payload: CropUpdate, db: Session = Depends(get_db), _=Depends(require_permission("users:read"))):
    crop = CropService(db).update(crop_id, payload)
    return success_response("Record updated successfully", CropRead.model_validate(crop).model_dump(mode="json"))


@router.delete("/{crop_id}")
def delete_crop(crop_id: UUID, db: Session = Depends(get_db), _=Depends(require_permission("users:read"))):
    CropService(db).delete(crop_id)
    return success_response("Record deleted successfully")
