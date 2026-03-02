from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from database import Engine, get_db
import schemas, models, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from oauth2 import require_role
from models import UserRole
from datetime import datetime

models.Base.metadata.create_all(bind=Engine)

app = FastAPI()

@app.post("/register",response_model=schemas.UserResponse)
def register_user(
    user: schemas.UserCreate,
    db:Session=Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.email==user.email).first()
    if db_user:
        raise HTTPException(status_code=409,detail="User already registered")
    hashed_pwd = oauth2.get_password_hashed(user.password)
    new_user =models.User(
        name = user.name,
        email = user.email,
        password = hashed_pwd,
        role = user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm=Depends(), 
    db: Session=Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    if not oauth2.verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/courses",response_model=schemas.CourseResponse)
def Enrollment(
    course:schemas.CourseCreate,
    db:Session=Depends(get_db),
    current_user: models.User = Depends(require_role(UserRole.teacher))
):
        new_course = models.Course(**course.model_dump(), teacher_id=current_user.id)
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
        
@app.post("/assignments", response_model=schemas.AssignmentResponse)
def add_assignment(
    assignment: schemas.AssignmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(UserRole.teacher))
):
    course = db.query(models.Course).filter(models.Course.id == assignment.course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course Not Found")
    
    if course.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only add assignments to your own courses")

    new_assignment = models.Assignment(**assignment.model_dump())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    return new_assignment

@app.get("/courses", response_model=list[schemas.CourseResponse])
def get_courses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role == UserRole.teacher:
        courses = db.query(models.Course).filter(models.Course.teacher_id == current_user.id).all()
        return courses

    if current_user.role == UserRole.student:
        courses = db.query(models.Course).all()
        return courses

    else:
        raise HTTPException(status_code=403, detail="Invalid Role")
    
@app.get("/assignments", response_model=list[schemas.AssignmentResponse])
def get_assignments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if current_user.role == UserRole.teacher:
        assignments = db.query(models.Assignment).join(models.Course).filter(models.Course.teacher_id == current_user.id).all()
        return assignments
    
    if current_user.role == UserRole.student:
        assignments = db.query(models.Assignment).all()
        return assignments

    else:
        raise HTTPException(status_code=403, detail="Invalid Role")

@app.post("/assignment_submission", response_model=schemas.SubmissionResponse)
def submit_assignment(
    submission: schemas.SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role(UserRole.student))
):
    assignment = db.query(models.Assignment).filter(
        models.Assignment.id == submission.assignment_id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment Not Found")
    
    if assignment.due_date and datetime.utcnow() > assignment.due_date:
       raise HTTPException(
        status_code=400,
        detail="Submission deadline has passed"
    )

    existing = db.query(models.Submission).filter(
        models.Submission.assignment_id == submission.assignment_id,
        models.Submission.student_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="You Already Submitted This Assignment")

    new_submission = models.Submission(
        content=submission.content,
        student_id=current_user.id,
        assignment_id=submission.assignment_id
    )

    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return new_submission