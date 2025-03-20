import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime, timedelta
from repository.base_repository import setup_database
from service.input_service import insert_activity_data
from service.window_activity_service import insert_window_data
from jose import jwt, JWTError
import uvicorn

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
static_path = os.path.abspath("www")

mock_users = {
    "admin": {"username": "admin", "password": "password"}
}

app.mount("/static", StaticFiles(directory=static_path), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str):
    """Verifica se o token JWT é válido"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Retorna o usuário autenticado
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=302, detail="Redirecting to login", headers={"Location": "/login"})
    return token

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

@app.post("/api/activity")
async def receive_activity(data: List[ActivityData]):
    print("Dados recebidos:", data)
    insert_activity_data(data)
    return {"status": "sucesso", "received": len(data)}

@app.post("/api/window-activity")
async def receive_activity(data: List[WindowData]):
    print("Dados recebidos:", data)
    insert_window_data(data)
    return {"status": "sucesso", "received": len(data)}

@app.get("/api/reports")
async def get_reports(token: str = Depends(oauth2_scheme)):
    return {"message": "Endpoint de relatórios em desenvolvimento"}

@app.get("/login")
async def login_page():
    login_path = os.path.join("www/views", "login.html")
    return FileResponse(login_path)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    access_token = create_access_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def root(request: Request):
    token = request.cookies.get("access_token")
    if not token or not verify_token(token):
        return RedirectResponse(url="/login")
    main_path = os.path.join("www/views", "index.html")
    return FileResponse(main_path)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)