from typing import List
from fastapi import APIRouter, Depends
from app.services.user_service import UserService
from app.responses.user import UsersListResponse, UserResponse
from app.requests.user import UserCreate

router = APIRouter()



## List Users Route
@router.get("/", response_model = UsersListResponse)
async def listUsers( service: UserService = Depends(UserService) ):
    return await service.callFunction("list", {"skip": 0, "limit": 10})



## Create User Route
@router.post("/", response_model = UserResponse)
async def createUser( data: UserCreate, service: UserService = Depends(UserService) ):
    return await service.callFunction("create", {"user": data})



## Get User Route
@router.get("/{user_id}", response_model = UserResponse)
async def getUser( user_id: int, service: UserService = Depends(UserService) ):
    return await service.callFunction("getById", {"user_id": user_id})



## Update User Route
@router.put("/{user_id}")
async def updateUser( user_id: int ):
    return {"user": {}, "user_id": user_id}



## Delete User Route
@router.delete("/{user_id}")
async def deleteUser( user_id: int ):
    return {"user": {}, "user_id": user_id}
