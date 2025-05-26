from fastapi import FastAPI
from api.v1.user import router as user
from api.v1.role import router as role
app = FastAPI()


app.include_router(user)
app.include_router(role)
@app.get("/")
async def root():
    return {"message": "Hello World"}
