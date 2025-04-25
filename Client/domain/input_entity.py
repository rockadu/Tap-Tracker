from pydantic import BaseModel, Field

class input_entity(BaseModel):
    logged_user: str
    mouse_clicks: int  = Field(0, ge=0)
    key_presses: int   = Field(0, ge=0)
    mouse_scroll: int  = Field(0, ge=0)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True