from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import JWTError, jwt
import openeo


router = APIRouter()


SECRET_KEY = "f7e3e2f7a4b3a0a5b2c1d0e4f5"
ALGORITHM = "HS256"


class Credentials(BaseModel):
    username: str
    password: str

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/auth/openeo")
async def auth_openeo(credentials: Credentials):

    try:
        connection = openeo.connect(url="openeo.dataspace.copernicus.eu")

        conn = connection.authenticate_oidc_client_credentials(
            client_id=credentials.username,
            client_secret=credentials.password
        )

        access_token = create_access_token(data={"sub": credentials.username})

        return {"access_token": access_token, "token_type": "bearer"}
    
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/auth/get_collections")
async def get_collections(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/openeo"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
    conn = connection.authenticate_oidc_access_token(token)

    return conn.list_collections()