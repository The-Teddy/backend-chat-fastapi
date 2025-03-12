from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from os import makedirs
import uuid
from pathlib import Path
from app.defaults import INTERNAL_ERROR_MESSAGE
from app.services import UserService
from app.services import TokenService

upload_router = APIRouter(prefix='/upload', tags=['upload'])

UPLOAD_FOLDER = Path("uploads")
PROFILE_FOLDER = UPLOAD_FOLDER / Path("profile")
makedirs(UPLOAD_FOLDER, exist_ok=True)
makedirs(PROFILE_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

@upload_router.post("/profile-photo")
async def upload_photo_profile(file: UploadFile = File(...), authenticated_user: dict = Depends(TokenService().get_current_user)):
    try:
        extension = file.filename.split(".")[-1]

        if extension.lower() not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail={"errors": "Formato de arquivo não permitido!"})

        file_extesion = Path(file.filename).suffix
        new_filename  = f"{uuid.uuid4()}{file_extesion}"
        file_path = PROFILE_FOLDER / new_filename

        with file_path.open('wb') as buffer:
            buffer.write(await file.read())

        updated_user = await UserService().update_profile_photo_user(file_path, authenticated_user['id'])

        return JSONResponse(status_code=200, content={"message": "Foto de perfil atualziada com sucesso!", "data": updated_user})
    
    except HTTPException as error:
        print(f"Erro ao trocar de foto no controller: {error}")

        raise HTTPException(status_code=error.status_code, detail=error.detail)

    except Exception as error:
        print(f"Erro ao trocar de foto no controller: {error}")
        raise HTTPException(status_code=500, detail={"errors": INTERNAL_ERROR_MESSAGE})