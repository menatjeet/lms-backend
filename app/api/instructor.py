from fastapi import APIRouter, Depends

from app.api.deps import require_role
from app.models.user import User, UserRole

router = APIRouter(
    prefix="/instructor",
    tags=["Instructor"]
)


@router.get("/dashboard")
def instructor_dashboard(
    current_user: User = Depends(
        require_role(
            UserRole.ADMIN,
            UserRole.INSTRUCTOR
        )
    )
):
    return {
        "message": "Welcome to Instructor Dashboard",
        "user": current_user.name,
        "role": current_user.role
    }