from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import UserRole, User
from app.schemas.enrollment import EnrollmentResponse
from app.api.deps import get_current_user, require_role
from app.schemas.enrollment import EnrollmentResponse, CourseStudentResponse

router = APIRouter(tags=["Enrollments"])

@router.post(
    "/courses/{course_id}/enroll",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED
)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.STUDENT))
):
    # Check if course exists
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check duplicate enrollment
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )

    # Create enrollment
    enrollment = Enrollment(
        student_id=current_user.id,
        course_id=course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment

@router.get(
    "/my-courses",
    response_model=list[EnrollmentResponse]
)
def get_my_courses(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(UserRole.STUDENT))
):
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == current_user.id
    ).all()

    return enrollments

@router.get(
    "/course/{course_id}/students",
    response_model=list[CourseStudentResponse]
)
def get_course_students(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_role(UserRole.ADMIN, UserRole.INSTRUCTOR)
    )
):
    # Check if course exists
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Instructor can only view students of own course
    if (
        current_user.role == UserRole.INSTRUCTOR
        and course.instructor_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot view students of this course"
        )

    # Get enrolled students
    students = db.query(
        User.id,
        User.name,
        User.email
    ).join(
        Enrollment,
        Enrollment.student_id == User.id
    ).filter(
        Enrollment.course_id == course_id
    ).all()

    return [
      {
        "id": student.id,
        "name": student.name,
        "email": student.email
      }
    for student in students
    ]