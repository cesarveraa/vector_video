from fastapi import FastAPI
from fastapi.responses import JSONResponse
import cv2
import os
from pydantic import BaseModel
from typing import List

app = FastAPI()

VIDEO_PATH = "video.mp4"

class DeskStatus(BaseModel):
    desk_id: int
    occupied: bool
    last_vacant_seconds: float

class OfficeAnalysis(BaseModel):
    total_desks: int
    total_occupied: int
    total_unoccupied: int
    desk_statuses: List[DeskStatus]

@app.get("/analyze", response_model=OfficeAnalysis)
def analyze_office():
    simulated_desks = [
        {"desk_id": 1, "occupied": True, "last_vacant_seconds": 0.0},
        {"desk_id": 2, "occupied": True, "last_vacant_seconds": 0.0},
        {"desk_id": 3, "occupied": False, "last_vacant_seconds": 300.0},
        {"desk_id": 4, "occupied": False, "last_vacant_seconds": 1200.0},
        {"desk_id": 5, "occupied": True, "last_vacant_seconds": 0.0},
    ]

    total_desks = len(simulated_desks)
    occupied = sum(1 for d in simulated_desks if d["occupied"])
    unoccupied = total_desks - occupied

    desk_statuses = [DeskStatus(**desk) for desk in simulated_desks]
    
    result = OfficeAnalysis(
        total_desks=total_desks,
        total_occupied=occupied,
        total_unoccupied=unoccupied,
        desk_statuses=desk_statuses
    )
    return result

@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"})
