from pydantic import BaseModel
from typing import Optional


class Restaurant(BaseModel):
    Restaurant_Name: str
    Res_Id:Optional[str]=None
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
    
    @field_validator("Pincode", mode="before")
    @classmethod
    def clean_pincode(cls, v):
        if v is None or v == "None":
            return None
        return str(v)
