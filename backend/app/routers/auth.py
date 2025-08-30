from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth_service import AuthService

router = APIRouter()



## User Login Route
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends(AuthService)):
    return await service.callFunction("login", {"form": form})