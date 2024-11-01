from fastapi import FastAPI
from app.routers import openeo_routes, openeo_auth, sign_up

app = FastAPI()
app.include_router(openeo_routes.router)
app.include_router(openeo_auth.router)
app.include_router(sign_up.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
