from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from schemas import MatchPayload
from services import compute_match_summary

app = FastAPI()

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
# ROUTES
# -----------------------------
@app.get("/")
def home():
    return {"message": "Cricket API Running 🚀"}


@app.post("/scoreboard")
def scoreboard(payload: MatchPayload):
    return compute_match_summary(payload.dict())