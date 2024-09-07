from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.Utils.config import settings
from app.Utils.authorization import authenticate_user, create_access_token
from app.api.v1.jobs import router as jobs_router
from app.Utils.database import get_database
import uvicorn

app = FastAPI()

app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])

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
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
