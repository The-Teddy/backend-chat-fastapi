from dotenv import load_dotenv
load_dotenv(override=True)
from app import create_app
from os import getenv

app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    FLASK_API_HOST = getenv("FLASK_API_HOST")
    FLASK_API_PORT = getenv('FLASK_API_PORT')
    
    

    uvicorn.run(app, host=FLASK_API_HOST, port=FLASK_API_PORT)