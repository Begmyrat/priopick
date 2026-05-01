from fastapi import APIRouter, Depends

from app.api.v1.deps import get_auth_service, get_current_user
from app.schemas.user import (
    RefreshRequest,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.services.auth import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    data: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    data: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh(data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/health")
async def health():
    return {"status": "healthy", "service": "auth"}