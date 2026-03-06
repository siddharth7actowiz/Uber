from pydantic import BaseModel
from typing import Optional


class Restaurant(BaseModel):
    Restaurant_Name: str
    Phone_No: Optional[str]
    Full_Address: Optional[str]
    Street_address: Optional[str]
    City: Optional[str]
    Country: Optional[str]
    Region: Optional[str]
    Pincode: Optional[int]
    Timing: Optional[str]
    ETA: Optional[str]
    Map: Optional[str]
    Dining_Modes: str
    Cuisions: str
    Category: str
    Featured_Category: str
    Currency: Optional[str]
