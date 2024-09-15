from fastapi import FastAPI
from app.routers import openeo_routes

app = FastAPI()
app.include_router(openeo_routes.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
