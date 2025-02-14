from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from app.schemas import LoginSchema
from app.services import AuthService
from app.defaults.default_messages import INTERNAL_ERROR_MESSAGE

auth_router = APIRouter(prefix="/auth")

@auth_router.post('/login')
async def login(user: LoginSchema):

    try:
        authenticated_user = await AuthService().authenticate_user(user.email, user.password)

        return JSONResponse(status_code=200, content=authenticated_user)

    except HTTPException as error:
        return error
    
    except Exception as error:
        print("login_error: ", error)

        raise HTTPException(status_code=500, detail={"errors": INTERNAL_ERROR_MESSAGE})