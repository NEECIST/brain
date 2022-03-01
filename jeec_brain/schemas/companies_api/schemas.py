from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class Company_Login_Form(BaseModel):
    username: Optional[str] = Field(None, description = "company's username")
    password: Optional[str] = Field(None, description = "company's password")

class Company_Login_Body(BaseModel):
    username: Optional[str] = Field(None, description = "company's username")
    password: Optional[str] = Field(None, description = "company's password")
    
class APIError(BaseModel):
    error: str = Field(None, description="Error")

class AuctionBidForm(BaseModel):
    value: str = Field(None, description = "value")
    is_anonymous: str = Field(None, description = "is anonymous")
    
class ActivityCodesCode(BaseModel):
    code:Optional[str] = Field(None, description = "code")

class UserIdForm(BaseModel):
    ist_id:str = Field(None, description = "ist id")

