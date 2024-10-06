from pydantic import BaseModel
from typing import Optional,ClassVar, Dict
from datetime import datetime

class Ramen(BaseModel):
    Ramen_id: int
    Soup: str
    Meat: str
    Spicy: int
    Typeid: ClassVar[Dict[str, int]] = {'Miso': 1, 'Shoyu': 2, 'Tonkatso': 3}  
    # it would be better if we could store this mapping in database, but since the time is limit we just store this info in code to save the cost of using database

class RamenCreate(BaseModel):
    Soup: str
    Meat: str
    Spicy: int

class Order(BaseModel): 
    Order_id: int
    Ramen_id: int
    Price:  Optional[int] = 12 
    Status: str
    Timestamp: Optional[datetime] 
     
    
class OrderCreate(BaseModel):
    Ramen_id: int

     