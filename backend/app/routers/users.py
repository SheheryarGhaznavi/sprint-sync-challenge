from fastapi import APIRouter, Depends
from app.services.user_service import UserService

router = APIRouter()



## List Users Route
@router.get("/")
async def listUsers( service: UserService = Depends(UserService) ):
    return await service.list()



## Create User Route
@router.post("/")
async def createUser():
    return {"user": {}}



## Get User Route
@router.get("/{user_id}")
async def getUser( user_id: int ):
    return {"user": {}, "user_id": user_id}



## Update User Route
@router.put("/{user_id}")
async def updateUser( user_id: int ):
    return {"user": {}, "user_id": user_id}



## Delete User Route
@router.delete("/{user_id}")
async def deleteUser( user_id: int ):
    return {"user": {}, "user_id": user_id}
