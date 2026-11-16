from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.api.deps import require_role , get_current_user
from app.models.user import User, UserRole
from app.models.course import Course
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonResponse, LessonUpdate

router = APIRouter(
    prefix="/courses",
    tags=["Lessons"]
)

lesson_router = APIRouter(
    prefix="/lessons",
    tags=["Lessons"]
)


@router.post(
    "/{course_id}/lessons",
    response_model=LessonResponse,
    status_code=status.HTTP_201_CREATED
)
def create_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN, UserRole.INSTRUCTOR)
    )
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if (
        current_user.role == UserRole.INSTRUCTOR.value
        and course.instructor_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage lessons in your own courses"
        )

    new_lesson = Lesson(
        course_id=course_id,
        title=lesson_data.title,
        content=lesson_data.content,
        order_no=lesson_data.order_no
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)

    return new_lesson

@router.get(
    "/{course_id}/lessons",
    response_model=list[LessonResponse]
)
def get_course_lessons(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    lessons = db.query(Lesson).filter(
        Lesson.course_id == course_id
    ).order_by(Lesson.order_no).all()

    return lessons

@lesson_router.put(
    "/lessons/{lesson_id}",
    response_model=LessonResponse
)
def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN, UserRole.INSTRUCTOR)
    )
):
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    course = db.query(Course).filter(
        Course.id == lesson.course_id
    ).first()

    if (
        current_user.role == UserRole.INSTRUCTOR.value
        and course.instructor_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update lessons in your own courses"
        )

    lesson.title = lesson_data.title
    lesson.content = lesson_data.content
    lesson.order_no = lesson_data.order_no

    db.commit()
    db.refresh(lesson)

    return lesson

@lesson_router.delete("/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN, UserRole.INSTRUCTOR)
    )
):
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    course = db.query(Course).filter(
        Course.id == lesson.course_id
    ).first()

    if (
        current_user.role == UserRole.INSTRUCTOR.value
        and course.instructor_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete lessons in your own courses"
        )

    db.delete(lesson)
    db.commit()

    return {
        "message": "Lesson deleted successfully"
    }