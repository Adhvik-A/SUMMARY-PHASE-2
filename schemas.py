from typing import List, Optional
from pydantic import BaseModel


class Batter(BaseModel):
    name: str
    runs: int
    balls: int
    fours: int = 0
    sixes: int = 0


class Bowler(BaseModel):
    name: str
    balls: int
    wickets: int
    runs_conceded: int


class MatchPayload(BaseModel):
    batting_team: str
    bowling_team: str

    total_runs: int
    wickets: int
    balls_bowled: int

    total_overs: int = 20
    target: Optional[int] = None
    extras: int = 0

    batters: List[Batter]
    bowlers: List[Bowler]

    recent_balls: List[str] = []