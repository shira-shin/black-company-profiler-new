# server/main.py

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from server.models import ProfileRequest, ProfileResponse
from server.services.fetch_official import fetch_official
from server.services.fetch_search import fetch_search
from server.services.scoring import compute_score, rank_from_score
from server.services.comment import make_comment

load_dotenv()
app = FastAPI(title="Black Company Profiler")

@app.post("/profile", response_model=ProfileResponse)
async def profile(req: ProfileRequest):
    # Prepare default placeholders
    resp = {
        "company": req.company,
        "score": 0.0,
        "rank": "D",
        "comment": "",
        "breakdown": {"growth": 0.0, "profit": 0.0, "info": 0.0}
    }
    try:
        official = await fetch_official(req.company, req.statsDataId)
        search_text = await fetch_search(req.company)
        score, breakdown = compute_score(official, req.preset)
        rank = rank_from_score(score)
        comment = await make_comment(
            company=req.company,
            score=score,
            rank=rank,
            breakdown=breakdown,
            context=search_text
        )
        # Fill in the real values
        resp.update({
            "score": score,
            "rank": rank,
            "comment": comment,
            "breakdown": breakdown
        })
    except Exception as e:
        # On any error, return the placeholders with an error comment
        resp["comment"] = f"Error occurred: {str(e)}"
    return resp
