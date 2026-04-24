README.md
Markdown
# 📘 Cricket Score Analytics API

### ● API Objective
This API generates a complete cricket innings summary using ball-by-ball events.  
It calculates score, run rate, player stats, phases, and extras — all from raw data.

---

### ● Endpoints
* **GET** `/`
* **GET** `/health`
* **POST** `/scoreboard`

---

### ● Input Schema (Example)
```json
{
  "match_id": "match_01",
  "innings_id": "innings_1",
  "batting_team": "RCB",
  "bowling_team": "MI",
  "include_extras": true,
  "events": [
    {
      "striker_id": "p1",
      "striker": "Virat Kohli",
      "bowler_id": "p101",
      "bowler": "Bumrah",
      "runs_off_bat": 1,
      "extras": 0,
      "is_legal_delivery": true,
      "wicket_fell": false
    },
    {
      "striker_id": "p2",
      "striker": "Faf du Plessis",
      "bowler_id": "p101",
      "bowler": "Bumrah",
      "runs_off_bat": 0,
      "extras": 1,
      "extra_type": "wide",
      "is_legal_delivery": false,
      "wicket_fell": false
    }
  ]
}
● Output Schema (Example)
JSON
{
  "meta": {
    "api": "event-match-summary",
    "version": "3.1",
    "status": "success"
  },
  "data": {
    "match_id": "match_01",
    "innings_id": "innings_1",
    "batting_team": "RCB",
    "bowling_team": "MI",
    "score": "6/0",
    "overs": "0.2",
    "run_rate": 18.0,
    "total_runs": 6,
    "wickets": 0,
    "fours": 1,
    "sixes": 0,
    "legal_balls": 2,
    "recent_balls": ["1", "0+1", "4"],
    "batters": [
      {
        "player_id": "p2",
        "name": "Faf du Plessis",
        "runs": 4,
        "balls": 1,
        "fours": 1,
        "sixes": 0,
        "strike_rate": 400.0
      }
    ],
    "bowlers": [
      {
        "player_id": "p101",
        "name": "Bumrah",
        "balls": 2,
        "runs_conceded": 6,
        "wickets": 0,
        "economy": 18.0
      }
    ],
    "top_batter": {
      "player_id": "p2",
      "name": "Faf du Plessis",
      "runs": 4
    },
    "top_bowler": {
      "player_id": "p101",
      "name": "Bumrah",
      "wickets": 0
    },
    "phases": {
      "powerplay": {
        "runs": 6,
        "balls": 2,
        "overs": "0.2",
        "run_rate": 18.0
      },
      "middle": {
        "runs": 0,
        "balls": 0,
        "overs": "0.0",
        "run_rate": 0
      },
      "death": {
        "runs": 0,
        "balls": 0,
        "overs": "0.0",
        "run_rate": 0
      }
    },
    "extras": {
      "total": 1,
      "breakdown": {
        "wide": 1,
        "no_ball": 0,
        "bye": 0,
        "leg_bye": 0
      }
    }
  },
  "errors": null
}
● GET Endpoints
Root GET /

JSON
{
  "meta": {
    "api": "cricket-score-api",
    "version": "3.1",
    "status": "running"
  },
  "message": "Event-based Cricket Analytics API",
  "endpoints": ["/health", "/scoreboard"]
}
Health GET /health

JSON
{
  "status": "ok"
}
🔴 Validation Errors
400 Bad Request

Runs or extras negative

Invalid extra_type

Empty events list

Wicket with runs > 0

Same batting & bowling team

JSON
{
  "detail": "Runs/extras cannot be negative"
}
422 Validation Error

Missing required fields

Invalid data types

Enum mismatch

500 Internal Error

Unexpected server failure

🔗 Integration Usage
Using Fetch (Frontend)

JavaScript
fetch("[https://score-phase-2.onrender.com/scoreboard](https://score-phase-2.onrender.com/scoreboard)", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(payload)
}).then(res => res.json()).then(data => console.log(data)).catch(err => console.error(err));
Using Axios

JavaScript
import axios from "axios";

axios.post("[https://score-phase-2.onrender.com/scoreboard](https://score-phase-2.onrender.com/scoreboard)", payload)
  .then(res => console.log(res.data))
  .catch(err => console.error(err));
UI Usage (Frontend)
Main Header: Show score, overs, run rate

Tables: Display batters & bowlers

Cards: Highlight top batter and top bowler

Timeline: Render recent balls

Tooltips: Show extras breakdown

Visuals: Use phases for charts

Best Practices
Keep events in order

Use consistent player_id

Validate before sending

Use include_extras only when needed

# Conclusion
This is a fully event-driven cricket analytics engine, not just a scoreboard.

It is accurate, scalable, and ready for real-time systems.