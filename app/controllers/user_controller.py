from fastapi import APIRouter, HTTPException
from app.schemas import UserRegisterSchema, UsernameSchema
from app.services import UserService
from fastapi.responses import JSONResponse
from app.defaults import INTERNAL_ERROR_MESSAGE
from app.services import TokenService
from jose import jwt
from pymongo.errors import DuplicateKeyError

user_router = APIRouter(prefix='/users')

@user_router.post('/')
async def create(user: UserRegisterSchema):      

    try:
        await UserService().create_user(user)

        return JSONResponse(status_code=201, content={"message": "Usuário criado com sucesso"})
    
    except DuplicateKeyError as error:
        print(error)
        raise HTTPException(status_code=409, detail={"errors": str(error)})

    
    except Exception as error:
        print(f"create_user_error: {error}")
        raise HTTPException(status_code=500, detail={"errors": INTERNAL_ERROR_MESSAGE})
    

@user_router.post('/validate-username/')
async def validate_username(username: UsernameSchema):

    try:
        found_username = await UserService().get_user_by_username(username.username)

        if found_username:
            return JSONResponse(content={"indisponible_username": "O nome de usuário já está em uso"}, status_code=200)

        return JSONResponse(content={"disponible_username": "Nome de usuário disponível"}, status_code=200)
   
    except Exception as error:
        print("user_controler_validate_username: ", error)
        raise HTTPException(status_code=500, detail={"errors": INTERNAL_ERROR_MESSAGE})
    
@user_router.get('/verify-email/{token}')
async def verify_email(token: str):

    try:
        user_token = await TokenService().get_user_by_token(token)
        user       = await UserService().get_user_by_email(user_token['email'])
        
        if user['email_verified']:
            return JSONResponse(content={"message": "E-mail já verificado"}, status_code=200)
        
        await UserService().verify_email_user(user_token['email'])
       

        return JSONResponse(content={"message": "E-mail verificado com sucesso"}, status_code=200)

    except jwt.ExpiredSignatureError:
        print("Token Expirado!")
        raise HTTPException(status_code=401, detail={"errors": "Token Expirado! Um novo Token foi enviado para o seu e-mail", "resend": True})
    
    except jwt.InvalidTokenError:
        print("Token inválido")
        raise HTTPException(status_code=400, detail={"errors": "Token inválido"})
    
    except Exception as error:
        print(f"Erro ao verificar e-mail: {error}")
        raise HTTPException(status_code=500, detail={"errors": INTERNAL_ERROR_MESSAGE})