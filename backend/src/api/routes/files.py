from fastapi import APIRouter, Request, UploadFile

from src.services.files import FileServiceDep

router = APIRouter(prefix="/upload", tags=["File Upload"])


@router.post("/")
async def upload_file(
    request: Request,
    service: FileServiceDep,
    file: UploadFile,
):
    return await service.create(str(request.base_url), file)
