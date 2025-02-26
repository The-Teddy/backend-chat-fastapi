from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import mongodb, create_user_indexies
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):

        await mongodb.connect()
        await create_user_indexies()
        yield
        await mongodb.disconnect()

    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware, 
        allow_origins=["http://localhost:3000", "http://192.168.3.6:3000"], 
        allow_credentials=True, 
        allow_methods=["*"],
        allow_headers=["*"]    
    )
    app.mount("/uploads/profile", StaticFiles(directory="uploads/profile"), name="profile")
    

    from app.controllers import user_router, auth_router, email_router, upload_router
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(email_router)
    app.include_router(upload_router)


    return app