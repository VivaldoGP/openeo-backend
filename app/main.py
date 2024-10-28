from fastapi import FastAPI
from app.routers import openeo_routes, openeo_auth

app = FastAPI()
app.include_router(openeo_routes.router)
app.include_router(openeo_auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
