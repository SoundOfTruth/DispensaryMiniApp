from fastapi import APIRouter, Depends, Request, UploadFile

from src.api.dependencies import has_admin_permissions
from src.services.files import FileServiceDep

router = APIRouter(prefix="/upload", tags=["File Upload"])


@router.post("/", status_code=201, dependencies=[Depends(has_admin_permissions)])
async def upload_file(
    service: FileServiceDep,
    file: UploadFile,
    request: Request,
):
    return await service.create(str(request.base_url), file)
