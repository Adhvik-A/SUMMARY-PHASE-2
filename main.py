from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import MatchPayload
from services import compute_match_summary

app = FastAPI(
    title="Cricket Score Analytics API",
    description="Event-driven cricket innings engine that computes full match analytics from ball-by-ball data.",
    version="2.0"
)


# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# ROOT ENDPOINT
# -----------------------------
@app.get("/")
def root():
    return {
        "meta": {
            "api": "cricket-score-api",
            "version": "2.0",
            "status": "running"
        },
        "message": "Welcome to Cricket Score Analytics API",
        "available_endpoints": [
            "/health",
            "/scoreboard"
        ]
    }


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# MAIN API
# -----------------------------
@app.post("/scoreboard")
def scoreboard(payload: MatchPayload):
    try:
        return compute_match_summary(payload.model_dump())
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )