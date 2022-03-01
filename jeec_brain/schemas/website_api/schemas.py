from pydantic import BaseModel, Field
from typing import Optional,List,Dict
from uuid import UUID

class EventQuery(BaseModel):
    event: Optional[str] = Field(None, description="Search")

class ActivityQuery(EventQuery):
    name: Optional[str] = Field(None, description="Search")
    speaker: Optional[str] = Field(None, description="Search")
    company: Optional[str] = Field(None, description="Search")

class TeamQuery(BaseModel):
    name: Optional[str] = Field(None, description="Search")

class SpeakerDetail(BaseModel):
    name: str = Field(None, description="Speaker name")
    company: str = Field(None, description="Speaker company")
    company_link: str = Field(None, description="Speaker company link")
    position: str = Field(None, description="Speaker position")
    country: str = Field(None, description="Speaker country")
    bio: str = Field(None, description="Speaker bio")
    linkedin_url: str = Field(None, description="Speaker linkedin url")
    youtube_url: str = Field(None, description="Speaker youtube url")
    website_url: str = Field(None, description="Speaker website url")
    image: str = Field(None, description="Speaker image")
    company_logo: str = Field(None, description="Speaker company logo")

class SpeakerList(BaseModel):
    list: Dict[str,List[SpeakerDetail]] = Field(None, description="Speakers list")

class CompanyDetail(BaseModel):
    name: str = Field(None, description="Company name")
    partnership_tier: str = Field(None, description="Company partnership tier")
    logo: str = Field(None, description="Company logo")
    link: Optional[str] = Field(None, description="Company link")
    business_area: Optional[str] = Field(None, description="Company business area")

class CompaniesList(BaseModel):
    list: Dict[str,List[CompanyDetail]] = Field(None, description="Companies list")

class RewardsDetail(BaseModel):
    name: Optional[Dict[str,str]] = Field(None, description="Reward name")
    image: Optional[Dict[str,str]] = Field(None, description="Reward image")
    
class RewardsList(BaseModel):
    list: Dict[str,List[RewardsDetail]] = Field(None, description="Companies list")

class ActivityDetail(BaseModel):
    name: str = Field(None, description = "Activity name")
    description: str = Field(None, description = "Activity Description")
    location: str = Field(None, description = "Activity Localization")
    day: int = Field(None, description = "Day of Activity")
    time: str = Field(None, description = "Time of Activity")
    end_time: str = Field(None, description = "Activity end time")
    type: int = Field(None, description = "Activity type")
    registration_open: bool = Field(None, description="Activity registration open")
    registration_link: str = Field(None, description="Activity registration link")
    zoom_link: str = Field(None, description="Activity zoom link")
    speakers: Dict[str,List[SpeakerDetail]] = Field(None, description="Activity speaker list")
    moderator: Optional[str] = Field(None, description="Activity moderator")
    reward: Dict[str,List[RewardsDetail]] = Field(None, description="Activity reward")
    companies: Dict[str,List[CompanyDetail]] = Field(None, description="Activity company list")

class ActivityList(BaseModel):
    list: Dict[str,List[ActivityDetail]] = Field(None, description="Activity list")

class MemberDetail(BaseModel):
    name: str  = Field(None, description = "Member name")
    linkedin_url: str = Field(None, description = "Member's Linkedin ")
    image: str = Field(None, description = "Member's image ")

class MemberList(BaseModel):
    list: Dict[str,List[MemberDetail]] = Field(None, description="Member list")

class TeamDetail(BaseModel):
    name: str  = Field(None, description = "Team name")
    description: str = Field(None, description = "Team description")
    members:Dict[str,List[MemberDetail]] = Field(None, description="Member list")

class TeamList(BaseModel):
    list: Dict[str,List[TeamDetail]] = Field(None, description="Team list")

class ActivityType(BaseModel):
    name: str  = Field(None, description = "Activity name") 
    show_in_home: bool = Field(None, description = "Activity (?)") 
    show_in_schedule: bool = Field(None, description = "Activity (?)") 

class ActivityTypeList(BaseModel):
    list: Dict[str,List[ ActivityType]] = Field(None, description="Activity type list")

class EventDetail(BaseModel):
    name: str = Field(None, description = "Event's name")
    start_date: str = Field(None, description = "Event's start date")
    end_date: str = Field(None, description = "Event's end date")
    email: str = Field(None, description = "Event's email")
    location: str = Field(None, description = "Event's location")
    facebook_link: str = Field(None, description = "Event's facebook")
    facebook_event_link: str = Field(None, description = "Event's facebook link")
    youtube_link: str = Field(None, description = "Event's youtube link")
    instagram_link: str = Field(None, description = "Event's instagram link")
    logo: str = Field(None, description = "Event's logo")
    mobile_logo: str = Field(None, description = "Event's mobile logo")
    schedule: str = Field(None, description = "Event's schedule")
    blueprint: str = Field(None, description = "Event's blueprint")
    activity_types:  Dict[str,List[ ActivityType]] = Field(None, description="Activity type list")
    dates: str = Field(None, description = "Event's date")
    show_schedule: bool = Field(None, description = "Activity schedule") 
    show_registration: bool = Field(None, description = "Activity registration") 

class EventDetailList(BaseModel):
    list: Dict[str,List[ EventDetail]] = Field(None, description="Event list")