from typing import Any
from pydantic import BaseModel, Field, model_validator

class Gum(BaseModel):
    """كيان يمثل حبة الطاقة العادية أو الخارقة"""
    
    grid_x: int
    grid_y: int
    
    is_super: bool = Field(default=False)
    is_eaten: bool = Field(default=False)
    
    points: int = Field(default=10)

    @model_validator(mode="after")
    def adjust_points(self) -> "Gum":
        """إذا كانت الحبة خارقة، نرفع قيمتها التلقائية إلى 50 (ما لم يتم تمرير قيمة أخرى)"""
        if self.is_super and self.points == 10:
            self.points = 50
        return self