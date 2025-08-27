from fastapi import FastAPI

app = FastAPI(title="Sprint Sync API", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Sprint Sync API"}