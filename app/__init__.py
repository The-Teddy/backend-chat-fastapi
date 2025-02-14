from fastapi import FastAPI
from app.config import mongodb
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):

        await mongodb.connect()
        yield
        await mongodb.disconnect()

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=["http://localhost:3000"], 
        allow_credentials=True, 
        allow_methods=["*"],
        allow_headers=["*"]    
    )

    

    from app.controllers import user_router, auth_router
    app.include_router(user_router)
    app.include_router(auth_router)


    return app