from pydantic import BaseModel, Field

#Modelo para dados de atividade
class WindowData(BaseModel):
    timestamp: str = Field(..., alias="Timestamp")
    logged_user: str = Field(..., alias="LoggedUser")
    window_title: str = Field(..., alias="WindowTitle")
    application_name: str = Field(..., alias="ApplicationName")
    activity_duration: int = Field(..., alias="ActivityDuration")
    
    class Config:
        allow_population_by_field_name = True