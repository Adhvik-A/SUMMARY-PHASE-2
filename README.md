 Cricket Summary API
● API Objective
This is a real-time Cricket Summary API that generates a complete innings summary from ball-by-ball events. It calculates score, run rate, wickets, phases, player stats, and extras dynamically.
--------------------------------------------------------------------------------
● Endpoints
GET / GET /health POST /summary
--------------------------------------------------------------------------------
● Input Schema
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
    }
  ]
}
● Output Schema
{
  "meta": {
    "api": "summary-api",
    "version": "1.0",
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
    "recent_balls": ["1", "4"],

    "batters": [],
    "bowlers": [],

    "top_batter": {},
    "top_bowler": {},

    "phases": {
      "powerplay": {},
      "middle": {},
      "death": {}
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
Root

GET /

{
  "status": "running",
  "api": "summary-api"
}
Health

GET /health

{
  "status": "ok"
}
● Validation Errors
400 Bad Request
Negative runs/extras
Invalid extra_type
Empty events list
Wicket with runs > 0
Same batting & bowling team
{
  "detail": "Runs/extras cannot be negative"
}
422 Validation Error
Missing fields
Invalid data types
Enum mismatch
500 Internal Error
Unexpected server failure
● Integration Usage
Fetch (Frontend)
fetch("https://score-phase-2.onrender.com/summary", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(payload)
})
.then(res => res.json())
.then(data => console.log(data));
Axios
axios.post("https://score-phase-2.onrender.com/summary", payload)
  .then(res => console.log(res.data))
  .catch(err => console.error(err));
● Frontend Usage
Live scoreboard rendering
Player stats dashboard
Top batter & bowler highlight
Phase-wise charts
Extras visualization
Recent ball tracking
🚀 Conclusion

The Summary API is a fully event-driven cricket analytics engine that converts raw ball-by-ball data into structured match intelligence in real time.
