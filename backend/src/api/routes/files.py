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
    scheme = request.headers.get("X-Forwarded-Proto", "http")
    host = request.headers.get("X-Forwarded-Host", request.headers.get("Host", "localhost"))
    base_url = str(request.base_url)
    if scheme and host:
        base_url = f"{scheme}://{host}/"
    return await service.create(base_url, file)
