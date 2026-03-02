from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from sqlalchemy import Enum   
from enum import Enum as PyEnum 

class UserRole(str, PyEnum):
    student = "student"
    teacher = "teacher"
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.student)
    courses = relationship("Course", back_populates="creator", cascade="all, delete")
    submissions = relationship("Submission", back_populates="student")
    

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    batch = Column(String)
    professor = Column(String)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="courses")    
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    issue_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete")
    
class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    student = relationship("User", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")