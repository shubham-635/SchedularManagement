from fastapi import APIRouter, Depends, HTTPException, status
from app.Utils.database import get_database
from app.Utils.authorization import verify_token
from bson import ObjectId
from app.Utils.config import Job

router = APIRouter(
    dependencies=[Depends(verify_token)]
)

@router.get("/")
async def get_jobs(db=Depends(get_database)):
    jobs = await db.get_collection('jobs').find({}).to_list(length=100)
    return jobs

@router.get("/{job_id}")
async def get_job(job_id: str, db=Depends(get_database)):
    job = await db.get_collection('jobs').find_one({"_id": ObjectId(job_id)})
    if job:
        return job
    else:
        raise HTTPException(status_code=404, detail="Job not found")

@router.post("/")
async def create_job(job_data: Job, db=Depends(get_database)):
    result = await db.get_collection('jobs').insert_one(job_data.dict())
    return {"job_id": str(result.inserted_id)}
