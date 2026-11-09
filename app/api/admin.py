from fastapi import APIRouter , Depends

from app.api.deps import require_role
from app.models.user import UserRole, User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    )
):
    return {
        "message": "Welcome to Admin Dashboard",
        "user": current_user.name,
        "role": current_user.role
    }