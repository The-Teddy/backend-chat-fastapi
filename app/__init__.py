from fastapi import FastAPI
from app.config import mongodb
from contextlib import asynccontextmanager

def create_app():

    @asynccontextmanager
    async def lifespan(app: FastAPI):

        await mongodb.connect()
        yield
        await mongodb.disconnect()

    app = FastAPI(lifespan=lifespan)

    

    from app.controllers import user_router
    app.include_router(user_router)


    return app