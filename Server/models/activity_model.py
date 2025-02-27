from pydantic import BaseModel, Field

class ActivityData(BaseModel):
    timestamp: str = Field(..., alias="Timestamp")
    logged_user: str = Field(..., alias="LoggedUser")
    mouse_clicks: int = Field(..., alias="MouseClicks")
    key_presses: int = Field(..., alias="KeyPresses")
    mouse_scroll: int = Field(..., alias="MouseScroll")
    
    class Config:
        allow_population_by_field_name = True