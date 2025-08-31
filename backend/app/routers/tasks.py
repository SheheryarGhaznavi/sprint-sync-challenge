from fastapi import APIRouter, Depends

from app.services.task_service import TaskService
from app.responses.task import TasksListResponse, TaskResponse
from app.requests.task import TaskRequest
from app.utils.deps import getCurrentUser
from app.models.user import User

router = APIRouter()



## List Tasks Route
@router.get("/", response_model = TasksListResponse)
async def listTasks( service: TaskService = Depends(TaskService), current_user: User = Depends(getCurrentUser) ):
    return await service.callFunction("list", {"user": current_user})



## Create Task Route
@router.post("/", response_model = TaskResponse)
async def createTask( data: TaskRequest, service: TaskService = Depends(TaskService), current_user: User = Depends(getCurrentUser) ):
    return await service.callFunction("create", {"user": current_user, "task": data})



## Get Task Route
@router.get("/{task_id}", response_model = TaskResponse)
async def getTask( task_id: int, service: TaskService = Depends(TaskService), current_user: User = Depends(getCurrentUser) ):
    return await service.callFunction("getById", {"user": current_user, "task_id": task_id})



## Update Task Route
@router.put("/{task_id}", response_model = TaskResponse)
async def updateTask( task_id: int, data: TaskRequest, service: TaskService = Depends(TaskService), current_user: User = Depends(getCurrentUser)  ):
    return await service.callFunction("update", {"user": current_user, "task_id": task_id, "task_data": data})



## Delete Task Route
@router.delete("/{task_id}", response_model = TaskResponse)
async def deleteTask( task_id: int, service: TaskService = Depends(TaskService), current_user: User = Depends(getCurrentUser) ):
    return await service.callFunction("delete", {"user": current_user, "task_id": task_id})



## Update Task Status Route
@router.post("/{task_id}/status")
async def updateTaskStatus( task_id: int ):
    return {"task": {}, "task_id": task_id}
