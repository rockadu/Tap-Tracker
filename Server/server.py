from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from jose import jwt
import uvicorn

app = FastAPI()

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens. Substitua por uma lista específica se necessário.
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"]   # Permitir todos os headers
)

# Configurações JWT
SECRET_KEY = "secret-key-tap-tracker"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Mock de usuários (substituir pelo banco de dados depois)
mock_users = {
    "admin": {"username": "admin", "password": "password"}
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo para dados de atividade
class ActivityData(BaseModel):
    timestamp: str = Field(..., alias="Timestamp")
    logged_user: str = Field(..., alias="LoggedUser")
    mouse_clicks: int = Field(..., alias="MouseClicks")
    key_presses: int = Field(..., alias="KeyPresses")
    mouse_scroll: int = Field(..., alias="MouseScroll")
    
    class Config:
        allow_population_by_field_name = True

#Modelo para dados de atividade
class WindowData(BaseModel):
    timestamp: str = Field(..., alias="Timestamp")
    logged_user: str = Field(..., alias="LoggedUser")
    window_title: str = Field(..., alias="WindowTitle")
    application_name: str = Field(..., alias="ApplicationName")
    activity_duration: int = Field(..., alias="ActivityDuration")
    
    class Config:
        allow_population_by_field_name = True

# Função para autenticação de usuário
def authenticate_user(username: str, password: str):
    user = mock_users.get(username)
    if user and user["password"] == password:
        return user
    return None

# Função para criar token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Endpoint para login e geração de token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    access_token = create_access_token({"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint para recebimento de dados de atividade
@app.post("/api/activity")
async def receive_activity(data: List[ActivityData]):
    # Aqui será feita a validação e armazenamento no banco de dados
    print("Dados recebidos:", data)
    return {"status": "sucesso", "received": len(data)}

@app.post("/api/window-activity")
async def receive_activity(data: List[WindowData]):
    # Aqui será feita a validação e armazenamento no banco de dados
    print("Dados recebidos:", data)
    return {"status": "sucesso", "received": len(data)}

# Endpoint para relatórios (a ser detalhado)
@app.get("/api/reports")
async def get_reports(token: str = Depends(oauth2_scheme)):
    # Aqui será implementada a lógica de geração de relatórios
    return {"message": "Endpoint de relatórios em desenvolvimento"}

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Tap Tracker Server!"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)