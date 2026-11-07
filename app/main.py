from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.connection import engine

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