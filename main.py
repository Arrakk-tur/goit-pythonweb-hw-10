
from fastapi import FastAPI
from src.api import api_contacts

app = FastAPI()

app.include_router(api_contacts.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8800, reload=True)