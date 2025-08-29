from fastapi import APIRouter

router = APIRouter()



## List Tasks Route
@router.get("/")
async def listTasks():
    return {"tasks": []}



## Create Task Route
@router.post("/")
async def createTask():
    return {"task": {}}



## Get Task Route
@router.get("/{task_id}")
async def getTask( task_id: int ):
    return {"task": {}, "task_id": task_id}



## Update Task Route
@router.put("/{task_id}")
async def updateTask( task_id: int ):
    return {"task": {}, "task_id": task_id}



## Delete Task Route
@router.delete("/{task_id}")
async def deleteTask( task_id: int ):
    return {"task": {}, "task_id": task_id}



## Update Task Status Route
@router.post("/{task_id}/status")
async def updateTaskStatus( task_id: int ):
    return {"task": {}, "task_id": task_id}
