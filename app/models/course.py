from datetime import datetime , timezone
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    title : Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    description : Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    instructor_id: Mapped[int]= mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )