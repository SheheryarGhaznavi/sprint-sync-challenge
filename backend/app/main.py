from fastapi import FastAPI

from app.routers import auth, users, tasks, ai
from app.core.logging import registerLogging

app = FastAPI(title="Sprint Sync API", version="0.1.0")



# Middlewares

# Structured logging middleware
registerLogging(app)



# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authorization"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])


@app.get("/")
async def root():
    return {"message": "Sprint Sync API"}