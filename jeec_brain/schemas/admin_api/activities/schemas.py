from pydantic import BaseModel, Field
from uuid import UUID

class ActivityTypePath(BaseModel):
    activity_type_external_id: UUID = Field(None, description="Activity type external ID")

class ActivityPath(BaseModel):
    activity_external_id: UUID = Field(None, description="Activity external ID")

class CodePath(BaseModel):
    code: UUID = Field(None, description="Activity code")