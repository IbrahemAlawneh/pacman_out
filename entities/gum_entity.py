from pydantic import BaseModel, Field


class Gum(BaseModel):
    grid_x: int
    grid_y: int
    points: int = Field(default=10)

    is_super: bool = Field(default=False)
    is_eaten: bool = Field(default=False)
