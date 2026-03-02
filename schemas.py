from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from models import UserRole

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes=True

class SubmissionCreate(BaseModel):
    assignment_id: int
    content: str
    
class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    content: str
    submitted_at: datetime
    
    class Config:
        from_attributes= True
 
class AssignmentCreate(BaseModel):
    title: str
    course_id :int
    description: str
    due_date: datetime

class AssignmentResponse(BaseModel):
    id: int
    title: str
    description: str
    issue_date: datetime
    due_date: datetime
    course_id: int
    submissions: List[SubmissionResponse]= []

    class Config:
        from_attributes= True
                
class CourseCreate(BaseModel):
    title: str
    professor: Optional[str]= None
    batch: Optional[str]= None

class CourseResponse(BaseModel):
    id: int
    title:str
    batch: Optional[str]= None      
    professor:Optional[str]= None 
    teacher_id: int
    assignments: List[AssignmentResponse]= []

    class Config:
        from_attributes=True

class TokenData(BaseModel):
    id: Optional[int] = None
        