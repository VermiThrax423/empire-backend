"""
Defines request/response formats 
i.e. what the API accepts/returns
"""

from pydantic import BaseModel
from uuid import UUID

class PlayerCreate(BaseModel):
    email: str 


class CityResponse(BaseModel):
    id: UUID
    name: str 
    x: int 
    y: int 

    class Config:
        from_attributes = True