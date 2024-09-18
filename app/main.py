from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.Utils.config import settings
from app.Utils.authorization import authenticate_user, create_access_token
from app.api.v1.jobs import router as jobs_router
from app.Utils.database import get_database, check_and_create_db
import uvicorn
from app.Utils.scheduler import start_scheduler, stop_scheduler

app = FastAPI()

app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])


# @app.on_event("startup")
# async def startup_db_client():
    # await check_and_create_db()


@app.on_event("startup")
async def startup_event():
    start_scheduler()
    await check_and_create_db()

@app.on_event("shutdown")
async def shutdown_event():
    # Stop the scheduler gracefully
    stop_scheduler()


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_database)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
