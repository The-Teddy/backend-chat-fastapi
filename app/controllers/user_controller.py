from fastapi import APIRouter, HTTPException
from app.schemas import UserRegisterSchema, UsernameSchema
from app.services import UserService
from fastapi.responses import JSONResponse
from app.defaults import INTERNAL_ERROR_MESSAGE


user_router = APIRouter(prefix='/users')

@user_router.post('/')
async def create(user: UserRegisterSchema):      

    try:
        created_user =  await UserService().create_user(user)

        return created_user
    
    except HTTPException as error:

        return error
    
    except Exception as error:

        raise HTTPException(status_code=500, detail={"errors": INTERNAL_ERROR_MESSAGE})
    

@user_router.post('/validate-username/')
async def validate_username(username: UsernameSchema):

    try:
        print(username.username)
        found_username = await UserService().get_user_by_username(username.username)

        if found_username:
            return JSONResponse(content={"indisponible_username": "O nome de usuário já está em uso"}, status_code=200)

        return JSONResponse(content={"disponible_username": "Nome de usuário disponível"}, status_code=200)
    except Exception as error:
        print("user_controler_validate_username: ", error)
        
        raise HTTPException(status_code=500, detail={"errors": INTERNAL_ERROR_MESSAGE})