from schemas import MatchPayload


# -----------------------------
# HELPERS
# -----------------------------
def balls_to_overs(balls: int) -> str:
    return f"{balls // 6}.{balls % 6}"


def run_rate(runs: int, balls: int) -> float:
    return round((runs / balls) * 6, 2) if balls else 0


def get_phase(ball: int):
    if ball < 36:
        return "powerplay"
    elif ball < 90:
        return "middle"
    return "death"


# -----------------------------
# MAIN SERVICE
# -----------------------------
def compute_match_summary(payload: dict):

    runs = payload["total_runs"]
    wickets = payload["wickets"]
    balls = payload["balls_bowled"]

    batters = payload["batters"]
    bowlers = payload["bowlers"]

    overs = balls_to_overs(balls)
    rr = run_rate(runs, balls)

    # -----------------------------
    # BATTERS
    # -----------------------------
    batter_list = []
    for b in batters:
        sr = (b["runs"] / b["balls"] * 100) if b["balls"] else 0

        batter_list.append({
            "name": b["name"],
            "runs": b["runs"],
            "balls": b["balls"],
            "fours": b["fours"],
            "sixes": b["sixes"],
            "strike_rate": round(sr, 2)
        })

    # -----------------------------
    # BOWLERS
    # -----------------------------
    bowler_list = []
    for b in bowlers:
        overs_bowled = b["balls"] / 6 if b["balls"] else 0
        eco = (b["runs_conceded"] / overs_bowled) if overs_bowled else 0

        bowler_list.append({
            "name": b["name"],
            "balls": b["balls"],
            "wickets": b["wickets"],
            "runs_conceded": b["runs_conceded"],
            "economy": round(eco, 2)
        })

    # -----------------------------
    # BEST PLAYERS
    # -----------------------------
    top_batter = max(batter_list, key=lambda x: x["runs"], default=None)
    top_bowler = max(bowler_list, key=lambda x: x["wickets"], default=None)

    # -----------------------------
    # TOTAL STATS
    # -----------------------------
    fours = sum(b["fours"] for b in batters)
    sixes = sum(b["sixes"] for b in batters)

    # -----------------------------
    # PHASES
    # -----------------------------
    phases = {
        "powerplay": {"runs": 0, "balls": 0},
        "middle": {"runs": 0, "balls": 0},
        "death": {"runs": 0, "balls": 0},
    }

    for i in range(balls):
        phase = get_phase(i)
        phases[phase]["balls"] += 1

    for k in phases:
        b = phases[k]["balls"]
        ratio = b / balls if balls else 0
        phases[k]["runs"] = int(runs * ratio)
        phases[k]["overs"] = balls_to_overs(b)
        phases[k]["run_rate"] = run_rate(phases[k]["runs"], b)

    # -----------------------------
    # CHASE
    # -----------------------------
    target = payload.get("target")

    runs_needed = balls_left = req_rr = None

    if target:
        runs_needed = target - runs
        balls_left = payload["total_overs"] * 6 - balls

        if balls_left > 0:
            req_rr = round((runs_needed / balls_left) * 6, 2)

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
    return {
        "batting_team": payload["batting_team"],
        "bowling_team": payload["bowling_team"],

        "score": f"{runs}/{wickets}",
        "overs": overs,
        "run_rate": rr,

        "total_runs": runs,
        "wickets": wickets,

        "extras": payload["extras"],
        "fours": fours,
        "sixes": sixes,

        "legal_balls": balls,
        "recent_balls": payload.get("recent_balls", [])[-12:],

        "target": target,
        "runs_needed": runs_needed,
        "balls_remaining": balls_left,
        "required_run_rate": req_rr,

        "batters": batter_list,
        "bowlers": bowler_list,

        "top_batter": top_batter,
        "top_bowler": top_bowler,

        "phases": phases
    }