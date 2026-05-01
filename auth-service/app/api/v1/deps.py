from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.auth import AuthService

bearer_scheme = HTTPBearer()


async def get_auth_service(
    db: AsyncSession = Depends(get_db)
) -> AuthService:
    return AuthService(db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.get_current_user(credentials.credentials)