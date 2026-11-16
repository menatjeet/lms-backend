from pydantic import BaseModel, ConfigDict, Field

class LessonCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=1)
    order_no: int = Field(ge=1)


class LessonUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=1)
    order_no: int = Field(ge=1)

class LessonResponse(BaseModel):
    id: int
    course_id: int
    title: str
    content: str

model_config = ConfigDict(from_attributes=True)    

