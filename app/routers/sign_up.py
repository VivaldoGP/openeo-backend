from fastapi import APIRouter
from app.schemas import User


router = APIRouter()


@router.post("/register")
async def register(user: User):
    print(user.username, user.email)
    return {"message": "User registered successfully"}