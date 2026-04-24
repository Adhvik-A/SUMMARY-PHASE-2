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


def compute_match_summary(payload: dict):

    events = payload["events"]
    include_extras = payload.get("include_extras", False)

    total_runs = 0
    wickets = 0
    legal_balls = 0
    total_extras = 0

    batters = {}
    bowlers = {}

    phases = {
        "powerplay": {"runs": 0, "balls": 0},
        "middle": {"runs": 0, "balls": 0},
        "death": {"runs": 0, "balls": 0},
    }

    extras_breakdown = {
        "wide": 0,
        "no_ball": 0,
        "bye": 0,
        "leg_bye": 0
    }

    recent_balls = []

    for e in events:

        runs = e["runs_off_bat"]
        extras = e["extras"]
        extra_type = e.get("extra_type")
        is_legal = e["is_legal_delivery"]
        wicket = e["wicket_fell"]

        striker_id = e["striker_id"]
        bowler_id = e["bowler_id"]

        total_runs += runs + extras
        total_extras += extras

        # Phase tracking
        phase = get_phase(legal_balls)
        phases[phase]["runs"] += runs + extras

        # Batter
        if striker_id not in batters:
            batters[striker_id] = {
                "player_id": striker_id,
                "name": e["striker"],
                "runs": 0,
                "balls": 0,
                "fours": 0,
                "sixes": 0
            }

        batters[striker_id]["runs"] += runs

        if is_legal:
            batters[striker_id]["balls"] += 1
            phases[phase]["balls"] += 1

        if runs == 4:
            batters[striker_id]["fours"] += 1
        elif runs == 6:
            batters[striker_id]["sixes"] += 1

        # Bowler
        if bowler_id not in bowlers:
            bowlers[bowler_id] = {
                "player_id": bowler_id,
                "name": e["bowler"],
                "balls": 0,
                "runs_conceded": 0,
                "wickets": 0
            }

        bowlers[bowler_id]["runs_conceded"] += runs + extras

        if is_legal:
            bowlers[bowler_id]["balls"] += 1
            legal_balls += 1

        if wicket:
            wickets += 1
            bowlers[bowler_id]["wickets"] += 1

        # Extras breakdown
        if include_extras and extra_type:
            extras_breakdown[extra_type] += extras

        # Recent balls
        symbol = "W" if wicket else str(runs)
        if extras > 0:
            symbol = f"{symbol}+{extras}"

        recent_balls.append(symbol)
        if len(recent_balls) > 6:
            recent_balls.pop(0)

    overs = balls_to_overs(legal_balls)
    rr = run_rate(total_runs, legal_balls)

    # Batters
    batter_list = []
    for b in batters.values():
        sr = (b["runs"] / b["balls"] * 100) if b["balls"] else 0
        b["strike_rate"] = round(sr, 2)
        batter_list.append(b)

    # Bowlers
    bowler_list = []
    for b in bowlers.values():
        overs_bowled = b["balls"] / 6 if b["balls"] else 0
        eco = (b["runs_conceded"] / overs_bowled) if overs_bowled else 0
        b["economy"] = round(eco, 2)
        bowler_list.append(b)

    # Top performers
    top_batter = max(batter_list, key=lambda x: (x["runs"], x["strike_rate"]), default=None)
    top_bowler = max(bowler_list, key=lambda x: (x["wickets"], -x["economy"]), default=None)

    # Totals
    fours = sum(b["fours"] for b in batter_list)
    sixes = sum(b["sixes"] for b in batter_list)

    # Phase finalize
    for k in phases:
        b = phases[k]["balls"]
        phases[k]["overs"] = balls_to_overs(b)
        phases[k]["run_rate"] = run_rate(phases[k]["runs"], b)

    data = {
        "match_id": payload["match_id"],
        "innings_id": payload["innings_id"],
        "batting_team": payload["batting_team"],
        "bowling_team": payload["bowling_team"],
        "score": f"{total_runs}/{wickets}",
        "overs": overs,
        "run_rate": rr,
        "total_runs": total_runs,
        "wickets": wickets,
        "fours": fours,
        "sixes": sixes,
        "legal_balls": legal_balls,
        "recent_balls": recent_balls,
        "batters": batter_list,
        "bowlers": bowler_list,
        "top_batter": top_batter,
        "top_bowler": top_bowler,
        "phases": phases
    }

    if include_extras:
        data["extras"] = {
            "total": total_extras,
            "breakdown": extras_breakdown
        }

    return {
        "meta": {
            "api": "event-match-summary",
            "version": "3.1",
            "status": "success"
        },
        "data": data,
        "errors": None
    }