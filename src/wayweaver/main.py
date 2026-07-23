from fastapi import FastAPI

def create_app() -> FastAPI:
    application = FastAPI(title="WayWeaver") 

    @application.get("/health/live")
    async def health_live() -> dict[str, str]:
        return {"status": "ok"}

    return application

app = create_app()