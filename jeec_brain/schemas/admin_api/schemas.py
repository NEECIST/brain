from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class APIError(BaseModel):
    error: str= Field(None, description="Error information")

class CompanyName(BaseModel):
    name: str= Field(None, description="name")

class ZoomUrl(BaseModel):
    name: str= Field(None, description="name")

class CompanyName(BaseModel):
    name: str= Field(None, description="name")

class CompanyName(BaseModel):
    name: str= Field(None, description="name")

class AdminLoginForm(BaseModel):
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")

class AdminLoginBody(BaseModel):
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")

class ActivityQuery(BaseModel):
    name: Optional[str] = Field(None, description="name")
    event: Optional[UUID] = Field(None, description = "event_id")

class ActivityTypeQuery(BaseModel):
    event_id: Optional[UUID] = Field(None, description = "event id")

class ActivityTypeForm(BaseModel):
    name: Optional[str] = Field(None, description="name")
    description: Optional[str] = Field(None, description="description")
    price: Optional[float] = Field(None, description="price")
    show_in_home: Optional[bool] = Field(None, description="show_in_home")
    show_in_schedule: Optional[bool] = Field(None, description="show_in_schedule")
    show_in_app: Optional[bool] = Field(None, description="show_in_app")
    event_id: Optional[int] = Field(None, description="event_id")

class ActivityForm(BaseModel):
    name: Optional[str]= Field(None, description="name")
    description: Optional[str]= Field(None, description="description")
    location: Optional[str]= Field(None, description="location")
    day: Optional[str]= Field(None, description="day")
    time: Optional[str]= Field(None, description="time")
    end_time: Optional[str]= Field(None, description="end_time")
    registration_link: Optional[str]= Field(None, description="registraion_link")
    registration_open: Optional[str]= Field(None, description="registration_open")
    points: Optional[int]= Field(None, description="points")
    quest: Optional[str]= Field(None, description="quest")
    chat: Optional[str]= Field(None, description="chat")
    zoom_link: Optional[str]= Field(None, description="zoom_link")
    reward_id: Optional[int]= Field(None, description="reward_id")
    moderator: Optional[str]= Field(None, description="moderator")
    activity_type_external_id: Optional[UUID]= Field(None, description="activity_type_external_id")
    companies: Optional[List[str]]= Field(None, description="companies")
    zoom_urls: Optional[List[str]]= Field(None, description = "zoom_urls")
    speakers: Optional[List[str]]= Field(None, description = "speakers")
    tags: Optional[List[str]]= Field(None, description = "tags")

class ActivityCodes(BaseModel):
    activity_codes: Optional[list] = Field(None, description = "activity_codes")

class ActivityCodesNumber(BaseModel):
    number: Optional[int] = Field(None, description = "number")

class SuccessStr(BaseModel):
    success: str = Field(None, description = "Success")

class SuccessDict(BaseModel):
    success: Dict[str,str] = Field(None, description = "Success")

class AuctionForm(BaseModel):
    name: Optional[str] = Field(None, description="name")
    description: Optional[str] = Field(None, description="description")
    starting_date: Optional[str] = Field(None, description="starting_date")
    closing_date: Optional[str] = Field(None, description="closing_date")
    starting_time: Optional[str] = Field(None, description="starting_time")
    closing_time: Optional[str] = Field(None, description="closing_time")
    minimum_value: Optional[str] = Field(None, description="minimum_value")

class CompanyExternalIdForm(BaseModel):
    company_external_id: Optional[UUID]= Field(None, description="company_external_id")

class CompanySearchForm(BaseModel):
    name: Optional[str]= Field(None, description="name")

class CompanyForm(BaseModel):
    name: Optional[str]= Field(None, description="name")
    link: Optional[str]= Field(None, description="link")
    email: Optional[str]= Field(None, description="email")
    business_area: Optional[str]= Field(None, description="business_area")
    show_in_website: Optional[str]= Field(None, description="show_in_website")
    partnership_tier: Optional[str]= Field(None, description="partnership_tier")
    evf_username: Optional[str]= Field(None, description="evf_username")
    evf_password: Optional[str]= Field(None, description="evf_password")
    cvs_access: Optional[str]= Field(None, description="cvs_access")

class EventQuery(BaseModel):
    name: Optional[str]= Field(None, description="name")

class EventForm(BaseModel):
    name: Optional[str]= Field(None, description="name")
    start_date: Optional[str]= Field(None, description="start_date")
    end_date: Optional[str]= Field(None, description="end_date")
    cvs_submission_start: Optional[str]= Field(None, description="cvs_submission_start")
    cvs_submission_end: Optional[str]= Field(None, description="cvs_submission_end")
    cvs_access_start: Optional[str]= Field(None, description="cvs_access_start")
    cvs_access_end: Optional[str]= Field(None, description="cvs_access_end")
    email: Optional[str]= Field(None, description="email")
    location: Optional[str]= Field(None, description="location")
    default: Optional[str]= Field(None, description="default")
    facebook_event_link: Optional[str]= Field(None, description="facebook_event_link")
    facebook_link: Optional[str]= Field(None, description="facebook_link")
    youtube_link: Optional[str]= Field(None, description="youtube_link")
    instagram_link: Optional[str]= Field(None, description="instagram_link")
    show_schedule: Optional[str]= Field(None, description="show_schedule")
    show_registrations: Optional[str]= Field(None, description="show_registrations")

class MealQuery(BaseModel):
    day: Optional[str]= Field(None, description="day")

class MealForm(BaseModel):
    type: Optional[str]= Field(None, description="type")
    location: Optional[str]= Field(None, description="location")
    day: Optional[str]= Field(None, description="day")
    time: Optional[str]= Field(None, description="time")
    registration_day: Optional[str]= Field(None, description="registration_day")
    registration_time: Optional[str]= Field(None, description="registration_time")
    company: Optional[List[str]]= Field(None, description="company")
    max_dish_quantity: Optional[List[str]]= Field(None, description="max_dish_quantity")
    dish_name: Optional[List[str]]= Field(None, description="dish_name")
    dish_description: Optional[List[str]]= Field(None, description="dish_description")
    dish_type: Optional[List[str]]= Field(None, description="dish_type")

class SpeakerSearchForm(BaseModel):
    name: Optional[str]= Field(None, description="name")

class SpeakerForm(BaseModel):
    name: Optional[str]= Field(None, description="name")
    company: Optional[str]= Field(None, description="company")
    company_link: Optional[str]= Field(None, description="company_link")
    position: Optional[str]= Field(None, description="position")
    country: Optional[str]= Field(None, description="country")
    bio: Optional[str]= Field(None, description="bio")
    linkedin_url: Optional[str]= Field(None, description="linkedin_url")
    youtube_url: Optional[str]= Field(None, description="youtube_url")
    website_url: Optional[str]= Field(None, description="website_url")
    spotlight: Optional[str]= Field(None, description="spotlight")

class StudentQuery(BaseModel):
    search: Optional[str]= Field(None, description="search")

class LevelUpdateForm(BaseModel):
    reward: Optional[str]= Field(None, description= "reward_id")

class LevelForm(LevelUpdateForm):
    value: Optional[str]= Field(None, description= "value")
    points: Optional[str]= Field(None, description= "points")

class TagForm(BaseModel):
    name: Optional[str]= Field(None, description= "name")

class RewardQuery(BaseModel):
    search: Optional[str]= Field(None, description= "search")

class RewardForm(BaseModel):
    name: Optional[str]= Field(None, description= "name")
    description: Optional[str]= Field(None, description= "description")
    link: Optional[str]= Field(None, description= "link")
    quantity: Optional[str]= Field(None, description= "quantity")

class JeecpotRewardForm(BaseModel):
    first_student_reward: Optional[str]= Field(None, description= "first_student_reward_id")
    second_student_reward: Optional[str]= Field(None, description= "second_student_reward_id")
    third_student_reward: Optional[str]= Field(None, description= "third_student_reward_id")
    first_squad_reward: Optional[str]= Field(None, description= "first_squad_reward_id")
    second_squad_reward: Optional[str]= Field(None, description= "second_squad_reward_id")
    third_squad_reward: Optional[str]= Field(None, description= "third_squad_reward_id")
    king_job_fair_reward: Optional[str]= Field(None, description= "king_job_fair_reward_id")
    king_knowledge_reward: Optional[str]= Field(None, description= "king_knowledge_reward_id")
    king_hacking_reward: Optional[str]= Field(None, description= "king_hacking_reward_id")
    king_networking_reward: Optional[str]= Field(None, description= "king_networking_reward_id")

class SquadRewardForm(BaseModel):
    reward: Optional[str]= Field(None, description= "reward")

class UserForm(BaseModel):
    name: Optional[str] = Field(None, description = "name")
    username: Optional[str] = Field(None, description = "username")
    email: Optional[str] = Field(None, description = "email")
    role: Optional[str] = Field(None, description = "name")
    post: Optional[str] = Field(None, description = "name")
    evf_username: Optional[str] = Field(None, description = "evf_username")
    evf_password: Optional[str] = Field(None, description = "evf_password")
    company_external_id: Optional[UUID] = Field(None, description = "company_external_id")
    food_manager: Optional[str] = Field(None, description = "food_manager")

class TeamForm(BaseModel):
    name: Optional[str] = Field(None, description = "name")
    event_id: Optional[int] = Field(None, description = "event id")


class CreateTeamForm(TeamForm):    
    description:  Optional[str] = Field(None, description = "name")
    website_priority:  Optional[int] = Field(None, description = "name")

class UpdateTeamForm(CreateTeamForm):
     event: Optional[int] = Field(None, description = "event id")

class CreateMemberForm(BaseModel):
    name: Optional[str] = Field(None, description = "name")
    ist_id: Optional[int] = Field(None, description = "ist_id")
    email: Optional[str] = Field(None, description = "email")
    linkedin_url: Optional[str] = Field(None, description = "linkedin url")

class AdminQuery(BaseModel):
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")
    


