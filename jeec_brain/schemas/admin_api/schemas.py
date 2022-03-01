from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional

class APIError(BaseModel):
    error: str= Field(..., description="Error information")

class AdminLoginForm(BaseModel):
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")

class AdminLoginBody(BaseModel):
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")

class ActivityQuery(BaseModel):
    name: Optional[str] = Field(None, description="name")
    event_id: Optional[int] = Field(None, description = "event_id")

class AdminQuery(BaseModel):
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")

class ActivityTypeForm(BaseModel):
    name: str = Field(None, description="name")
    description: str = Field(None, description="description")
    price: float = Field(None, description="price")
    show_in_home: bool = Field(None, description="show_in_home")
    show_in_schedule: bool = Field(None, description="show_in_schedule")
    show_in_app: bool = Field(None, description="show_in_app")
    event_id: int = Field(None, description="event_id")

class ActivityForm(BaseModel):
    name: str = Field(None, description="name")
    description: str = Field(None, description="description")
    location: str = Field(None, description="location")
    day: str = Field(None, description="day")
    time: str = Field(None, description="time")
    end_time: str= Field(None, description="end_time")
    registration_link: str = Field(None, description="registraion_link")
    registration_open: str = Field(None, description="registration_open")
    points: int= Field(None, description="points")
    quest: str= Field(None, description="quest")
    chat: str= Field(None, description="chat")
    zoom_link: str = Field(None, description="zoom_link")
    reward_id: int = Field(None, description="reward_id")
    moderator: str = Field(None, description="moderator")
    activity_type_external_id: UUID= Field(None, description="activity_type_external_id")
    companies: dict= Field(None, description="companies")
    zoom_urls: dict= Field(None, description = "zoom_urls")
    speakers: dict= Field(None, description = "speakers")
    tags: dict = Field(None, description = "tags")

class ActivityCodes(BaseModel):
    activity_codes: Optional[list] = Field(None, description = "activity_codes")

class ActivityCodesNumber(BaseModel):
    number: Optional[int] = Field(None, description = "number")

class SuccessStr(BaseModel):
    success: str = Field(None, description = "Success")

class SuccessDict(BaseModel):
    success: dict = Field(None, description = "Success")

class UserForm(BaseModel):
    name: str = Field(None, description = "name")
    username: str = Field(None, description = "username")
    email: str = Field(None, description = "email")
    role: str = Field(None, description = "role")
    post: str = Field(None, description = "post")
    evf_username: str = Field(None, description = "evf_username")
    evf_password: str = Field(None, description = "evf_password")
    company_external_id: UUID = Field(None, description = "company_external_id")
    food_manager: Optional[bool] = Field(None, description = "food_manager")

class TeamForm(BaseModel):
    name: str = Field(None, description = "name")
    event: int = Field(None, description = "event id")
    description:  Optional[str] = Field(None, description = "name")
    website_priority:  Optional[int] = Field(None, description = "website priority")


class CreateMemberForm(BaseModel):
    name: str = Field(None, description = "name")
    ist_id: int = Field(None, description = "ist_id")
    email: Optional[str] = Field(None, description = "email")
    linkedin_url: Optional[str] = Field(None, description = "linkedin url")


