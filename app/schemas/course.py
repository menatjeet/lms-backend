from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)


class CourseUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    instructor_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)