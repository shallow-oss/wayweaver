from fastapi import APIRouter

from wayweaver.schemas.health import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("/live", response_model=HealthResponse)
async def health_live() -> HealthResponse:
    return HealthResponse(status="ok")
