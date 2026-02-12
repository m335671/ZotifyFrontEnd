import uuid
from typing import Dict, Any
from datetime import datetime
from .models import Job

class JobsManager:
    def __init__(self):
        self.jobs: Dict[int, Job] = {}
        self.counter = 0
    
    def create(self, req: Dict[str, Any]) -> int:
        self.counter += 1
        job_id = self.counter
        job = Job(
            id=job_id,
            url=req["url"],
            type=req["type"],
            status="pending",
            created_at=datetime.utcnow(),
        )
        self.jobs[job_id] = job
        return job_id
    
    def update_status(self, job_id: int, status: str, **kwargs):
        if job_id not in self.jobs:
            return False
        job = self.jobs[job_id]
        for k, v in kwargs.items():
            setattr(job, k, v)
        job.status = status
        if status in ("done", "error"):
            job.finished_at = datetime.utcnow()
        return True
    
    def get_all(self) -> list[Job]:
        return list(self.jobs.values())

jobs_manager = JobsManager()