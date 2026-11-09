from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.connection import engine

from app.api.auth import router as auth_router
from app.api.instructor import router as instructor_router
from app.api.admin import router as admin_router

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
def home():
    return {"message": "LMS Backend is Running"}

@app.get("/db-check")
def database_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {"database": "Connected Successfully"}

    except Exception as error:
        return {
            "database": "Connection Failed",
            "error": str(error)
        }   


app.include_router(auth_router) 
app.include_router(admin_router)
app.include_router(instructor_router)
