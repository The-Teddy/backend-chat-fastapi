from dotenv import load_dotenv
load_dotenv(override=True)
from app import create_app
from os import getenv

app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    FAST_API_HOST = getenv("FAST_API_HOST")
    FAST_API_PORT = getenv('FAST_API_PORT')
    
    if not FAST_API_HOST or not FAST_API_PORT:
        raise RuntimeError("Configure as variáveis de ambiente FAST_API_HOST e FAST_API_PORT corretamente")
    

    uvicorn.run("main:app", host=FAST_API_HOST, port=int(FAST_API_PORT), reload=True, workers=5)