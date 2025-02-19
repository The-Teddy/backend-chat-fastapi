from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.defaults import INTERNAL_ERROR_MESSAGE
from app.services import TokenService
from app.schemas import ResendToken

email_router = APIRouter(prefix='/emails', tags=['Emails'])

@email_router.post('/resend-token')
async def resend_token(body: ResendToken):

    try:
        await TokenService().update_token_and_send_email(body.token)

        return JSONResponse(status_code=200, content={"message": "Novo token enviado com sucesso"})
    
    except ValueError as error:
        print(f"Erro ao enviar e-mail:  {error}")
        raise HTTPException(status_code=401, detail={"errors": str(error)})
    except Exception as error:
        print(f"Erro ao enviar e-mail:  {error}")
        raise HTTPException(status_code=500, detail={"errors": INTERNAL_ERROR_MESSAGE})
