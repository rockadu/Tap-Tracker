from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
from jose import jwt
import uvicorn
from Server.repository.base_repository import setup_database

from models.activity_model import ActivityData
from models.window_model import WindowData

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

SECRET_KEY = "secret-key-tap-tracker"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

mock_users = {
    "admin": {"username": "admin", "password": "password"}
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str):
    user = mock_users.get(username)
    if user and user["password"] == password:
        return user
    return None

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    access_token = create_access_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/activity")
async def receive_activity(data: List[ActivityData]):
    print("Dados recebidos:", data)
    return {"status": "sucesso", "received": len(data)}

@app.post("/api/window-activity")
async def receive_activity(data: List[WindowData]):
    print("Dados recebidos:", data)
    return {"status": "sucesso", "received": len(data)}

@app.get("/api/reports")
async def get_reports(token: str = Depends(oauth2_scheme)):
    return {"message": "Endpoint de relatórios em desenvolvimento"}

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Tap Tracker Server!"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)