import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import threading
import sys
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from .models import DownloadRequest, Job
from .jobs import jobs_manager

app = FastAPI(title="Zotify API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Zotify API prête"}


@app.get("/jobs")
async def get_jobs():
    return jobs_manager.get_all()


@app.post("/download")
async def start_download(req: DownloadRequest):
    job_id = jobs_manager.create(req.dict())
    
    def run_download():

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        try:
            jobs_manager.update_status(job_id, "running", progress=0)
            
            # Validation output_dir
            output_path = Path(req.output_dir) if req.output_dir else Path("./downloads")
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Commande Zotify
            cmd = [
                sys.executable, "-m", "zotify",
                "--client-id", req.client_id or "",
                "-rp", str(output_path.absolute()),  
                "-q", req.quality,
                "-rt", str(req.realtime),
                "--bulk-wait-time", str(req.bulk_wait_time),
                req.url
            ]
            
            print(f"\n{'='*60}")
            print(f"JOB {job_id} - COMMANDE ZOTIFY:")
            print(f"  {' '.join(cmd)}")
            print(f"{'='*60}\n")
            
            # Lance subprocess
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',       # <-- Force UTF-8 lecture
                env=env,                # <-- Force UTF-8 écriture Python
                cwd=req.output_dir or ".",
                bufsize=1
            )
            
            # Capture logs
            last_lines = []
            
            if process.stdout:
                for line in iter(process.stdout.readline, ''):
                    line = line.strip()
                    if line:
                        print(f"[JOB {job_id}] {line}")
                        last_lines.append(line)
                        if len(last_lines) > 10:
                            last_lines.pop(0)
                        
                        # Parse progress si présent
                        if '%' in line:
                            try:
                                parts = line.split('%')
                                if len(parts) > 0:
                                    progress_str = parts[0].split()[-1]
                                    progress = int(progress_str)
                                    jobs_manager.update_status(
                                        job_id, 
                                        "running", 
                                        progress=min(100, max(0, progress))
                                    )
                            except (ValueError, IndexError):
                                pass
            
            # Attend la fin
            rc = process.wait()
            
            print(f"\n{'='*60}")
            print(f"JOB {job_id} - TERMINÉ (exit code: {rc})")
            print(f"{'='*60}\n")
            
            if rc == 0:
                jobs_manager.update_status(job_id, "done", title="Download réussi")
            else:
                error_detail = last_lines[-1] if last_lines else "Unknown error"
                error_msg = f"Exit {rc}: {error_detail}"
                print(f"ERREUR JOB {job_id}: {error_msg}")
                jobs_manager.update_status(job_id, "error", error=error_msg)
                
        except FileNotFoundError as e:
            error_msg = f"Zotify introuvable: {e}"
            print(f"CRASH JOB {job_id}: {error_msg}")
            jobs_manager.update_status(job_id, "error", error=error_msg)
            
        except Exception as e:
            error_msg = f"Erreur inattendue: {str(e)}"
            print(f"CRASH JOB {job_id}: {error_msg}")
            jobs_manager.update_status(job_id, "error", error=error_msg)
    
    threading.Thread(target=run_download, daemon=True).start()
    return {"message": "Téléchargement lancé", "job_id": job_id}