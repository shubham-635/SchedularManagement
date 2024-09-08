from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.Utils.database import get_database
from app.Utils.config import Job
from datetime import datetime, timedelta
import asyncio

scheduler = AsyncIOScheduler()


async def execute_job(job: Job):
    print(f"Executing job: {job.name} at {datetime.now()}")
    # Logic to be executed for the Job e.g. Send Email Notifications or Push Notifications on Android device etc.


async def schedule_jobs():
    db = get_database()
    jobs = db["jobs"].find({"next_run": {"$lte": datetime.now()}})
    
    async for job in jobs:
        scheduler.add_job(
            execute_job,
            trigger=IntervalTrigger(minutes=job["interval"]),
            args=[job],
            id=str(job["_id"]),
            replace_existing=True
        )
        next_run_time = datetime.now() + timedelta(minutes=job["interval"])
        db["jobs"].update_one({"_id": job["_id"]}, {"$set": {"next_run": next_run_time}})


def start_scheduler():
    scheduler.add_job(
        schedule_jobs,
        trigger=IntervalTrigger(seconds=60), 
    )
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
