from fastapi import FastAPI

app = FastAPI(title="WayWeaver")

@app.get("/health/live")
async def health_live() -> dict[str, str]:
    return {"status": "ok"}