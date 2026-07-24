from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from wayweaver.db.session import get_db
from wayweaver.schemas.health import HealthResponse


router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/live", response_model=HealthResponse)
async def health_live() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get(
    "/ready",
    response_model=HealthResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Database is unavailable",
        },
    },
)
async def health_ready(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> HealthResponse:
    try:
        # 执行最小查询，验证数据库连接和查询能力。
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is not ready",
        ) from exc

    return HealthResponse(status="ok")