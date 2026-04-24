from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum


# -----------------------------
# ENUMS
# -----------------------------
class ExtraType(str, Enum):
    wide = "wide"
    no_ball = "no_ball"
    bye = "bye"
    leg_bye = "leg_bye"


# -----------------------------
# BALL EVENT
# -----------------------------
class BallEvent(BaseModel):
    striker_id: str
    striker: str

    bowler_id: str
    bowler: str

    runs_off_bat: int = Field(ge=0)
    extras: int = Field(default=0, ge=0)
    extra_type: Optional[ExtraType] = None

    is_legal_delivery: bool = True
    wicket_fell: bool = False

    @field_validator("runs_off_bat", "extras")
    @classmethod
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("Runs cannot be negative")
        return v


# -----------------------------
# MATCH PAYLOAD
# -----------------------------
class MatchPayload(BaseModel):
    match_id: str
    innings_id: str

    batting_team: str
    bowling_team: str

    events: List[BallEvent]

    include_extras: bool = False