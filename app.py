from fastapi import FastAPI

from routers import api_router

app = FastAPI()


@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": "Welcome to the OpusDoc API"
    }

app.include_router(api_router)