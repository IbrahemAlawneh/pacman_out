from typing import Any
from pydantic import BaseModel, Field, model_validator

class Gum(BaseModel):    
    grid_x: int
    grid_y: int
    points: int = Field(default=10)
    
    is_super: bool = Field(default=False)
    is_eaten: bool = Field(default=False)
