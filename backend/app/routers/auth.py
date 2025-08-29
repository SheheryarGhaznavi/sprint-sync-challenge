from fastapi import APIRouter

router = APIRouter()



## User Login Route
@router.get("/login")
async def listUsers():
    return {"message": 'login successful'}