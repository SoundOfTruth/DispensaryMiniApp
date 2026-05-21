from fastapi import APIRouter, Depends, UploadFile

from src.api.dependencies import BaseUrlDep, has_admin_permissions
from src.services.files import FileServiceDep

router = APIRouter(prefix="/upload", tags=["File Upload"])


@router.post("/", status_code=201, dependencies=[Depends(has_admin_permissions)])
async def upload_file(
    service: FileServiceDep,
    file: UploadFile,
    base_url: BaseUrlDep,
):
    return await service.create(base_url, file)
