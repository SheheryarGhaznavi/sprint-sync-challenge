from fastapi import APIRouter

router = APIRouter()



## List Users Route
@router.get("/")
async def listUsers():
    return {"users": []}



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
