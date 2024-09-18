from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.Utils.database import get_database
from app.Utils.config import Job
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()


async def execute_job(job: Job):
    print(f"Executing job: {job.name} at {datetime.now()}")
    # Logic to be executed for the Job e.g. Send Email Notifications or Push Notifications on Android device etc.


async def schedule_jobs():
    db = await get_database()
    
    jobs_collection = db.get_collection("jobs")
    
    jobs_cursor = jobs_collection.find({"next_run": {"$lte": datetime.utcnow()}})
    
    job_found = False

    async for job in jobs_cursor:
        job_found = True
        scheduler.add_job(
            execute_job,
            trigger=IntervalTrigger(minutes=job["interval"]),
            args=[job],
            id=str(job["_id"]),
            replace_existing=True
        )
        
        next_run_time = datetime.utcnow() + timedelta(minutes=job["interval"])
        await jobs_collection.update_one({"_id": job["_id"]}, {"$set": {"next_run": next_run_time}})
    
    if not job_found:
        print("No jobs found to schedule.\n\n\n")


def start_scheduler():
    print(f"Schedular Initiated: {datetime.now()}\n\n\n")
    scheduler.add_job(
        schedule_jobs,
        trigger=IntervalTrigger(seconds=60), 
    )
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
