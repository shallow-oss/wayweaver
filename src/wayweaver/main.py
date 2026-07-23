from fastapi import FastAPI

from wayweaver.api.router import api_router

def create_app() -> FastAPI:
    application = FastAPI(title="WayWeaver") 
    application.include_router(api_router)
    return application

app = create_app()