from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DownloadRequest(BaseModel):
    url: str
    type: str = "track"
    client_id: str
    output_dir: str = "./downloads"
    quality: str = "high"
    realtime: bool = True
    embed_metadata: bool = True
    download_lyrics: bool = False
    bulk_wait_time: int = 30


class Job(BaseModel):
    id: int
    url: str
    type: str
    status: str  # pending, running, done, error
    title: Optional[str] = None
    progress: Optional[int] = None
    error: Optional[str] = None
    created_at: datetime
    finished_at: Optional[datetime] = None